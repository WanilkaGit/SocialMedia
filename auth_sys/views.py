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
            password = form.cleaned_data['password']
            display_name = form.cleaned_data.get('display_name', '')

            # Створення користувача без Matrix
            user = User.objects.create_user(username=display_name, password=password)
            
            # Генерація JWT
            access_token = AccessToken.for_user(user)

            return render(request, 'auth_sys/login.html', {'form': form, 'access_token': str(access_token)})

    else:
        form = RegistrationForm()

    return render(request, 'auth_sys/registration.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            password = form.cleaned_data['password']
            display_name = form.cleaned_data.get('display_name', '')

            user = authenticate(username=display_name, password=password)
            if user is not None:
                login(request, user)
                return redirect("photozone_sys:photos")
            else:
                return HttpResponse("Failed to log in")

    return render(request, 'auth_sys/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('auth_sys:login')
    
    return render(request, 'auth_sys/logout.html')


def switch_account_view(request, account_id):
    try:
        new_account = SMUser.objects.get(id=account_id)
        if request.user.is_authenticated:
            # Перемикання на новий акаунт
            login(request, new_account)
            return redirect('photozone_sys:photos')
    except SMUser.DoesNotExist:
        return HttpResponse("Account does not exist")

    return redirect('auth_sys:login')
