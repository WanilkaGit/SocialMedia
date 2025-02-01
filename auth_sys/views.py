from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
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
from nio import AsyncClient, LoginResponse, RegisterResponse, LogoutResponse, LocalProtocolError
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
    
    if isinstance(response, LoginResponse):
        print(response.access_token)
        return response.access_token  # Повертаємо access_token
    else:
        return None  # Якщо логін не вдався, повертаємо None

def login_view(request):
    form = LoginForm(request.POST or None)  # Ініціалізуємо форму на початку

    if request.method == 'POST':
        if form.is_valid():
            matrix_user_id = form.cleaned_data['matrix_user_id']
            password = form.cleaned_data['password']

            # Отримуємо username без @ та домену
            username = matrix_user_id.split(':')[0][1:]

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(login_matrix(username=matrix_user_id, password=password))

            if response != None:
                # Перевірка існування MatrixUser

                user = authenticate(username=username, password=password)
                # Перевірка існування MatrixUser
                if user is not None:
                    login(request, user)
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
                    
                    # Додавання MatrixUser до SMUser
                    sm_user.matrix_user.add(matrix_user)
                    
                    # Зміна значення OneToOneField
                    sm_user.current_user = matrix_user
                    sm_user.save()  # Збереження змін
                    sm_user.current_user.access_token = response
                    sm_user.current_user.save()
                    print(sm_user.current_user.access_token)
                    print(response) 
                    
                    return redirect("messenger_sys:rooms")
                else:
                    return HttpResponse("Failed to log in")

    return render(request, 'auth_sys/login.html', {'form': form})

async def logout_matrix(access_token):
    client = AsyncClient("https://matrix.org")
    try:
        if access_token:
            client.access_token = access_token
            response = await client.logout()
            return response
    except LocalProtocolError:
        print("User was not logged in to Matrix.")
    finally:
        await client.close()

def logout_view(request):
    if request.method == 'POST':
        user = request.user
        
        if user.is_authenticated and hasattr(user, 'current_user'):
            matrix_user = user.current_user
            access_token = getattr(matrix_user, 'access_token', None)
            
            if access_token:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(logout_matrix(access_token))
                
                # Очистити access_token перед виходом
                matrix_user.access_token = ""
                matrix_user.save()
        
        logout(request)
        return redirect('auth_sys:login')
    
    return render(request, 'auth_sys/logout.html')
