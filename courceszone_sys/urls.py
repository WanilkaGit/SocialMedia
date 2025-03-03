from django.urls import path
from . import views

app_name = 'courcezone_sys'

urlpatterns = [
    # Тут будуть додані URL-шаблони для messanjer_sys
    path('audios-cos/', views._view, name='audio-cos'),
    path('videos-cos/', views._view, name='videos-cos'),
    path('photos-cos/', views._view, name='photos-cos'),
    path('3d-models-cos/', views._view, name='3d-models-cos'),

    path('codes-cos/', views._view, name='codes-cos'),
    path('finance-cos/', views._view, name='finance-cos'),
    path('cryptography-cos/', views._view, name='cryptography-cos'),
    path('scince-cos/', views._view, name='scince-cos'),
] 