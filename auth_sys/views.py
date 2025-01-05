from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import MatrixUser
from .forms import RegistrationForm, LoginForm
import json
import uuid
import requests
from django.conf import settings

def registration_view(request):
    print(1)
    if request.method == 'POST':
        print(2)
        form = RegistrationForm(request.POST)
        print(3)
        print(form.is_valid())
        if form.is_valid():
            print(4)
            matrix_user_id = form.cleaned_data['matrix_user_id']
            password = form.cleaned_data['password']
            display_name = form.cleaned_data['display_name']
            print(form.cleaned_data['recaptcha'])
            recaptcha_response = form.cleaned_data['recaptcha']
            print(5)
            # Перевірка reCAPTCHA
            recaptcha_secret = settings.RECAPTCHA_PRIVATE_KEY
            print(6)
            try:
                recaptcha_verification = requests.post(
                    'https://www.google.com/recaptcha/api/siteverify',
                    data={
                        'secret': recaptcha_secret,
                        'response': recaptcha_response
                    }
                )
                verification_result = recaptcha_verification.json()
                print(verification_result)
                if not verification_result.get('success'):
                    return render(
                        request, 
                        'auth_sys/registration.html', 
                        {'form': form, 'error': 'reCAPTCHA verification failed. Please try again.'}
                    )
                print(7)
            except requests.exceptions.RequestException:
                return render(
                    request, 
                    'auth_sys/registration.html', 
                    {'form': form, 'error': 'Error connecting to reCAPTCHA. Please try again later.'}
                )
            print(8)
            # Реєстрація користувача
            try:
                user = User.objects.create_user(
                    username=matrix_user_id.split(':')[0][1:], 
                    password=password
                )
                MatrixUser.objects.create(
                    matrix_user_id=matrix_user_id, 
                    user=user, 
                    display_name=display_name
                )
                print(9)
                return redirect('auth_sys:login')
                
            except Exception as e:
                return render(
                    request, 
                    'auth_sys/registration.html', 
                    {'form': form, 'error': 'An error occurred during registration. Please try again.'}
                )
        else:
            print(form.errors)
            print(10)
    else:
        form = RegistrationForm()
        

    return render(
        request, 
        'auth_sys/registration.html', 
        {'form': form, 'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY}
    )


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
