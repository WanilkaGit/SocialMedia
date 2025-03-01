from django.urls import path
from . import views

app_name = 'auth_sys'

urlpatterns = [
    # Тут будуть додані URL-шаблони для messanjer_sys
    path('login', views.logination_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register_view, name="register"),
]