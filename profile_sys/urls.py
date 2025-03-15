from django.urls import path
from .views import user_profile_view

app_name = 'profilezone_sys'

urlpatterns = [
    path('profile/', user_profile_view, name='profile'),
]