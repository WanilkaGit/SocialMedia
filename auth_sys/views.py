from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import MatrixUser
from .forms import RegistrationForm, LoginForm
import json
import uuid
import requests
from django.conf import settings
from nio import AsyncClient, LoginResponse, RegisterResponse
from rest_framework_simplejwt.tokens import AccessToken

async def register_user(user, password, device_name, auth_dict):
    client = AsyncClient("https://matrix.org", user)
    response = await client.register(user=user, password=password, device_name=device_name, auth_dict=auth_dict)
    return response

def registration_view(request):
    if request.method == 'POST':
        print(1)
        form = RegistrationForm(request.POST)
        print(1)
        print(form.is_valid)
        if form.is_valid():
            print(1)
            matrix_user_id = form.cleaned_data['matrix_user_id']
            password = form.cleaned_data['password']
            url = "https://matrix-nio.readthedocs.io/en/latest/nio.html#nio.Api.register"
            auth_dict = {
                    "type": "m.login.registration_token",
                    "registration_token": "access_token",
                    "session": "session-id-from-homeserver"
                }
            response = requests.post(url, json=auth_dict)
            if response.status_code == 200:
                print("Запит успішний!")
                print(response.json())
            else:
                print("Помилка:", response.status_code)
                print(response.text)
            device_name = form.cleaned_data.get('device_name', 'Web Client')
            
            

            # Виклик асинхронної функції реєстрації
            response = register_user(matrix_user_id, password, device_name=device_name, auth_dict=auth_dict)

            if isinstance(response, RegisterResponse):
                # Реєстрація успішна
                user = User.objects.create_user(username=matrix_user_id.split(':')[0][1:], password=password)
                MatrixUser.objects.create(
                    user=user,
                    matrix_user_id=matrix_user_id,
                    access_token=response.access_token,
                    device_id=response.device_id,
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

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            matrix_user_id = form.cleaned_data['matrix_user_id']
            password = form.cleaned_data['password']
            
            # Отримуємо username без @ та домену
            username = matrix_user_id.split(':')[0][1:]

            try:
                # Спроба автентифікації на Matrix сервері
                response = requests.post(
                    "https://matrix.org/_matrix/client/v3/login",
                    json={
                        "type": "m.login.password",
                        "identifier": {
                            "type": "m.id.user",
                            "user": username
                        },
                        "password": password,
                        "device_id": str(uuid.uuid4()),
                        "initial_device_display_name": "Web Client"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Якщо автентифікація успішна, створюємо або оновлюємо користувача
                    user, created = User.objects.get_or_create(
                        username=username,
                        defaults={'password': password}
                    )
                    
                    matrix_user, created = MatrixUser.objects.get_or_create(
                        matrix_user_id=matrix_user_id,
                        defaults={
                            'user': user,
                            'access_token': data['access_token'],
                            'device_id': data['device_id'],
                            'display_name': username
                        }
                    )
                    
                    if not created:
                        # Оновлюємо токен для існуючого користувача
                        matrix_user.access_token = data['access_token']
                        matrix_user.device_id = data['device_id']
                        matrix_user.save()
                    
                    login(request, user)
                    return redirect('index')
                else:
                    error_data = response.json()
                    return render(request, 'auth_sys/login.html', 
                                {'form': form, 'error': f'Помилка Matrix: {error_data.get("error", "Невірний логін або пароль")}'})

            except Exception as e:
                return render(request, 'auth_sys/login.html', 
                            {'form': form, 'error': f'Помилка: {str(e)}'})
    
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
