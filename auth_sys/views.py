from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import SMUser
from .forms import RegisterForm, LoginForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            login_name = form.cleaned_data.get("Login")
            authentificator = form.cleaned_data.get("authentificator")
            email = form.cleaned_data.get("Email")
            password = form.cleaned_data.get("Password1")

            # Перевіряємо, чи користувач вже існує
            if SMUser.objects.filter(autintificator=authentificator).exists():
                messages.error(request, "Користувач з таким логіном вже існує.")
                return render(request, "auth_sys/register.html", {"form": form})

            # Створюємо користувача коректним способом
            user = SMUser.objects.create_user(
                name=login_name,
                authentificator=authentificator,
                email=email,
                password=password  # Django автоматично хешує пароль
            )

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
            password = form.cleaned_data.get("password1")

            # Використовуємо `authenticate`
            user = authenticate(request, authentificator=authentificator, password=password)
            if user is not None:
                login(request, user)  # Авторизуємо користувача
                messages.success(request, "Успішний вхід!")
                return redirect("index")
            else:
                messages.error(request, "Неправильний логін або пароль.")

    else:
        form = LoginForm()

    return render(request, "auth_sys/login.html", {"form": form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Ви вийшли з системи.")
        return redirect('auth_sys:login')

    return render(request, 'auth_sys/logout.html')
