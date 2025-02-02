from django.urls import path
from . import views

app_name = 'photozone_sys'

urlpatterns = [
   path('photos/', views.photoszone_view, name='photos'),
   path('images/', views.imgs_4_designs_view, name='images')
] 