from django.urls import path
from .views import audio_view, music_view

app_name = 'audiozone_sys'  # Додайте цю строку для реєстрації простору імен

urlpatterns = [
    path('audio/', audio_view, name='audio'),
    path('music/', music_view, name='music'),
]
