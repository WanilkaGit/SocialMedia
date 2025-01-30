from django.urls import path
from . import views  # Імпортуйте ваші представлення, якщо вони є

app_name = 'messenger_sys'

urlpatterns = [
    path('rooms/', views.rooms_view, name='rooms'),
] 