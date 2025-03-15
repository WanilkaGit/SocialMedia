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
    def create_user(self, authentificator, password=None, **extra_fields):
        if not authentificator:
            raise ValueError('The authentificator field must be set')
        authentificator = self.normalize_email(authentificator)
        user = self.model(authentificator=authentificator, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, authentificator, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(authentificator, password, **extra_fields)

class SMUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, blank=True)
    authentificator = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    last_login_at = models.DateTimeField(auto_now=True)
    custom_pref = models.JSONField(default=dict)

    photos = models.ManyToManyField(Photos, blank=True)
    imgs = models.ManyToManyField(Imgs4Designs, blank=True)
    videos_long = models.ManyToManyField(LongVideo, blank=True)
    videos_short = models.ManyToManyField(ShortVideo, blank=True)
    audio = models.ManyToManyField(Audio, blank=True)
    music = models.ManyToManyField(Music, blank=True)
    project = models.ManyToManyField(Project, blank=True)

    objects = SMUserManager()

    USERNAME_FIELD = 'authentificator'
    REQUIRED_FIELDS = []

    def str(self):
        return self.email


class SavedAccount(models.Model):
    user = models.ForeignKey(SMUser, on_delete=models.CASCADE, related_name='saved_accounts')
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)  # Зберігаємо незашифрований пароль
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'username')