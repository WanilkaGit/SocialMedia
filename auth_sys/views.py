from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import MatrixUser, SMUser
from .forms import RegistrationForm, LoginForm
import json
import uuid
import requests
from django.conf import settings
from importlib import util
from rest_framework_simplejwt.tokens import AccessToken
from django.http import HttpResponse
from nio import AsyncClient, LoginResponse, RegisterResponse
import asyncio


def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            matrix_user_id = form.cleaned_data['matrix_user_id']
            password = form.cleaned_data['password']
            display_name = form.cleaned_data.get('display_name', '')

            # Виклик асинхронної функції реєстрації
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(register_user(matrix_user_id, password, display_name))

            if isinstance(response, RegisterResponse):
                # Реєстрація успішна
                user = User.objects.create_user(username=matrix_user_id.split(':')[0][1:], password=password)
                MatrixUser.objects.create(
                    user=user,
                    matrix_user_id=matrix_user_id,
                    access_token=response.access_token,
                    device_id=response.device_id,
                    display_name=display_name
                )
                
                # Генерація JWT
                access_token = AccessToken.for_user(user)

                return render(request, 'auth_sys/login.html', {'form': form, 'access_token': str(access_token)})
            else:
                # Обробка помилок реєстрації
                return render(request, 'auth_sys/registration.html', {'form': form, 'error': str(response)})

    else:
        form = RegistrationForm()

    return render(request, 'auth_sys/registration.html', {'form': form})


async def login_matrix(username, password):
    client = AsyncClient("https://matrix.org", username)
    response = await client.login(password)
    await client.close()
    return response

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            matrix_user_id = form.cleaned_data['matrix_user_id']
            password = form.cleaned_data['password']

            # Отримуємо username без @ та домену
            username = matrix_user_id.split(':')[0][1:]

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(login_matrix(username=matrix_user_id, password=password))

            if isinstance(response, LoginResponse):
                # Перевірка існування MatrixUser
                matrix_user, created = MatrixUser.objects.get_or_create(
                    name=username,
                    matrix_user_id=matrix_user_id,
                    defaults={'password': password}
                )
                
                # Перевірка існування SMUser
                sm_user, created = SMUser.objects.get_or_create(
                    display_name=username,
                    defaults={'custom_pref': {}}  # Використовуємо custom_pref як приклад
                )
                sm_user.matrix_user.add(matrix_user)

                return redirect("messenger_sys:chat")
            else:
                return HttpResponse("Failed to log in")
    else:
        form = LoginForm()

    return render(request, 'auth_sys/login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        try:
            matrix_user = MatrixUser.objects.get(user=request.user)
            
            # Вихід з Matrix сесії
            response = requests.post(
                "https://matrix.org/_matrix/client/r0/logout",
                headers={
                    "Authorization": f"Bearer {matrix_user.access_token}"
                }
            )
            
            # Видаляємо токен
            matrix_user.access_token = ""
            matrix_user.save()
            
        except Exception as e:
            print(f"Помилка при виході з Matrix: {str(e)}")
        
        logout(request)
    return redirect('index')
