"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

def index(request):
    return render(request, 'index.html')

def index_o_info(request):
    return render(request, 'index_o_info.html')

urlpatterns = [
    path('', index, name='index'),
    path('cos', index_o_info, name='index_o_info'),
    path('admin/', admin.site.urls),
    path('auth/', include('auth_sys.urls')),
    path('messenger/', include('messenger_sys.urls')),
    path('video/', include('videozone_sys.urls')),
    path('search/', include('searchzone_sys.urls')),
    path('projectzone/', include('projectzone_sys.urls')),
    path('profile/', include('profile_sys.urls')),
    path('photo/', include('photozone_sys.urls')),
    path('audio/', include('audiozone_sys.urls')),
    path('cos/', include('courceszone_sys.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
