from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

from projectzone_sys.models import Project
from audiozone_sys.models import Audio, Music
from videozone_sys.models import LongVideo, ShortVideo
from photozone_sys.models import Photos, Imgs4Designs

import uuid

class SMUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class SMUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    autintificator = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login_at = models.DateTimeField(auto_now=True)
    custom_pref = models.JSONField(default=dict)
    photos = models.ManyToManyField(Photos, blank=True)
    videos_long = models.ManyToManyField(LongVideo, blank=True)
    videos_short = models.ManyToManyField(ShortVideo, blank=True)
    audio = models.ManyToManyField(Audio, blank=True)
    music = models.ManyToManyField(Music, blank=True)
    project = models.ManyToManyField(Project, blank=True)

    objects = SMUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def str(self):
        return self.email