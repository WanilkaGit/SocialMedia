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
from nio import AsyncClient, LoginResponse, RegisterResponse
import asyncio
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


async def register_user(matrix_user_id, password, display_name):
    # Отримуємо username без @ та домену
    username = matrix_user_id.split(':')[0][1:]
    
    client = AsyncClient("https://matrix.org", matrix_user_id)
    try:
        response = await client.register(
            username=username,
            password=password,
            device_id=str(uuid.uuid4())
        )
        if display_name:
            await client.set_displayname(display_name)
        await client.close()
        return response
    except Exception as e:
        await client.close()
        return str(e)

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
                # Створюємо SMUser замість User
                username = matrix_user_id.split(':')[0][1:]
                
                # Створюємо MatrixUser
                matrix_user = MatrixUser.objects.create(
                    name=username,
                    matrix_user_id=matrix_user_id,
                    password=password,  # Зверніть увагу: краще зберігати хешований пароль
                    display_name=display_name if display_name else username
                )
                
                # Створюємо SMUser
                sm_user = SMUser.objects.create(
                    username=username,
                    display_name=display_name if display_name else username,
                    custom_pref={},
                    current_user=matrix_user
                )
                
                # Встановлюємо пароль для SMUser
                sm_user.set_password(password)
                sm_user.save()
                
                # Додаємо зв'язок між SMUser та MatrixUser
                sm_user.matrix_user.add(matrix_user)
                
                # Генерація JWT токену
                access_token = AccessToken.for_user(sm_user)
                
                return render(request, 'auth_sys/login.html', {
                    'form': LoginForm(),
                    'success_message': 'Реєстрація успішна! Тепер ви можете увійти.',
                    'access_token': str(access_token)
                })
            else:
                return render(request, 'auth_sys/registration.html', {
                    'form': form,
                    'error': f'Помилка реєстрації: {str(response)}'
                })
    else:
        form = RegistrationForm()

    return render(request, 'auth_sys/registration.html', {'form': form})


async def login_matrix(matrix_user_id, password):
    client = AsyncClient("https://matrix.org", matrix_user_id)
    try:
        response = await client.login(password=password)
        await client.close()
        return response
    except Exception as e:
        await client.close()
        return str(e)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            matrix_user_id = form.cleaned_data['matrix_user_id']
            password = form.cleaned_data['password']
            
            # Виклик асинхронної функції логіну
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(login_matrix(matrix_user_id, password))

            if isinstance(response, LoginResponse):
                try:
                    # Спробуємо знайти існуючого MatrixUser
                    matrix_user = MatrixUser.objects.get(matrix_user_id=matrix_user_id)
                    
                    # Оновлюємо токен доступу, якщо потрібно
                    matrix_user.access_token = response.access_token
                    matrix_user.save()
                    
                    # Знаходимо відповідного SMUser
                    sm_user = SMUser.objects.get(matrix_user=matrix_user)
                    
                    # Перевіряємо пароль
                    if sm_user.check_password(password):
                        # Виконуємо логін
                        login(request, sm_user)
                        
                        # Оновлюємо current_user
                        sm_user.current_user = matrix_user
                        sm_user.save()
                        
                        return redirect('messenger_sys:rooms')
                    else:
                        form.add_error(None, 'Невірний пароль')
                except MatrixUser.DoesNotExist:
                    form.add_error(None, 'Користувача не знайдено. Будь ласка, зареєструйтесь')
                except SMUser.DoesNotExist:
                    form.add_error(None, 'Помилка облікового запису. Зверніться до адміністратора')
            else:
                form.add_error(None, f'Помилка входу в Matrix: {str(response)}')
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
