from django.urls import path
from . import views

app_name = 'videozone_sys'

urlpatterns = [
   path('long-video/', views.long_videozone_view, name='long-video'),
   path('short-video/', views.short_videozone_view, name='short-video')
] 