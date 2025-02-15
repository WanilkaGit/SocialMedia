from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

from projectzone_sys.models import Project
from audiozone_sys.models import Audio, Music
from videozone_sys.models import LongVideo, ShortVideo
from photozone_sys.models import Photos

import uuid

# Create your models here.
class MatrixUser(models.Model):
    name = models.CharField(max_length=255)
    matrix_user_id = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    avatar_url = models.ImageField(upload_to='avatars/', null=True, blank=True)
    access_token = models.TextField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.matrix_user_id

class SMUserManager(BaseUserManager):
    def create_user(self, display_name, password=None, **extra_fields):
        if not display_name:
            raise ValueError("The Display Name must be set")
        user = self.model(display_name=display_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, display_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(display_name, password, **extra_fields)

class SMUser(AbstractBaseUser, PermissionsMixin):
    display_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    matrix_user = models.ManyToManyField('MatrixUser', related_name='sm_users', blank=True)
    last_login_at = models.DateTimeField(auto_now=True)
    current_user = models.OneToOneField('MatrixUser', on_delete=models.SET_NULL, related_name='current_sm_user', null=True, blank=True)
    custom_pref = models.JSONField(default=dict)
    photos = models.ManyToManyField(Photos, blank=True)
    videos_long = models.ManyToManyField(LongVideo, blank=True)
    videos_short = models.ManyToManyField(ShortVideo, blank=True)
    audio = models.ManyToManyField(Audio, blank=True)
    music = models.ManyToManyField(Music, blank=True)
  
    project = models.ManyToManyField(Project, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = SMUserManager()
    
    USERNAME_FIELD = 'display_name'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.display_name
