from django.urls import path
from . import views

app_name = 'messenger_sys'

urlpatterns = [
    path('rooms/', views.rooms_view, name='rooms'),
] 