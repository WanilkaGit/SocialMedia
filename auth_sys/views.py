from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse_lazy, reverse

from .models import SMUser, SavedAccount
from .forms import RegisterForm, LoginForm

import json

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)  # Авторизуємо нового користувача
            messages.success(request, "Реєстрація успішна!")
            return redirect("index")

    else:
        form = RegisterForm()

    return render(request, "auth_sys/register.html", {"form": form})

def logination_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            authentificator = form.cleaned_data.get("authentificator")
            password = form.cleaned_data.get("password")

            # Додайте логування
            print(f"Authentificator: {authentificator}, Password: {password}")

            user = authenticate(request, authentificator=authentificator, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Успішний вхід!")
                return redirect("index")
            else:
                messages.error(request, "Неправильний логін або пароль.")
                print("Аутентифікація не вдалася")
    else:
        form = LoginForm()

    return render(request, "auth_sys/login.html", {"form": form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Ви вийшли з системи.")
        return redirect('auth_sys:login')

    return render(request, 'auth_sys/logout.html')


def switch_account(request, username):
    if request.method == 'POST':
        try:
            # Отримуємо збережений акаунт
            saved_account = get_object_or_404(SavedAccount, user=request.user, username=username)
            User = get_user_model()
            next_user = get_object_or_404(User, username=username)
            
            # Перевіряємо пароль
            if next_user.check_password(saved_account.password):
                logout(request)
                login(request, next_user)
                return JsonResponse({
                    'status': 'success',
                    'redirect_url': reverse('profile', kwargs={'username': next_user.username})
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Помилка автентифікації'
                })
                
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    
    return JsonResponse({'status': 'error', 'message': 'Метод не дозволений'})
