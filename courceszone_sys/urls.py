from django.urls import path
from . import views

app_name = 'courceszone_sys'

urlpatterns = [
    path('ncource/', views.ncourse_view, name='ncource'),
    path('nlesson/', views.nlesson_view, name='nlesson'),

    path('audios-cos/', views.audiocos_view, name='audios-cos'),
    path('videos-cos/', views.videocos_view, name='videos-cos'),
    path('photos-cos/', views.photocos_view, name='photos-cos'),
    path('3d-models-cos/', views.model3dcos_view, name='3d-models-cos'),

    path('codes-cos/', views.codecos_view, name='codes-cos'),
    path('finance-cos/', views.financecos_view, name='finance-cos'),
    path('cryptography-cos/', views.cryptographycos_view, name='cryptography-cos'),
    path('scince-cos/', views.scincecos_view, name='scince-cos'),
]