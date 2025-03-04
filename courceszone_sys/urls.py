from django.urls import path
from . import views

app_name = 'courcezone_sys'

urlpatterns = [
    path('ncourse/', views.ncourse_view, name='ncourse'),
    path('nlesson/', views.nlesson_view, name='nlesson'),

    # path('audios-cos/', g name='audios-cos'),
    # path('videos-cos/', g name='videos-cos'),
    # path('photos-cos/', g, name='photos-cos'),
    # path('3d-models-cos/', g, name='3d-models-cos'),

    # path('codes-cos/', g, name='codes-cos'),
    # path('finance-cos/', g, name='finance-cos'),
    # path('cryptography-cos/', g, name='cryptography-cos'),
    # path('scince-cos/', g, name='scince-cos'),
] 