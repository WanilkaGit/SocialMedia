from django.urls import path
from . import views

app_name = 'projectszone_sys'

urlpatterns = [
    # Тут будуть додані URL-шаблони для messanjer_sys
    path('projects/', views.projectszone_view, name='projects'),
] 