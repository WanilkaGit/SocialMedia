from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from projectzone_sys.models import Project
from audiozone_sys.models import Audio, Music
from videozone_sys.models import LongVideo, ShortVideo
from photozone_sys.models import Photos

import uuid

# Create your models here.




class MatrixUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matrix_user_id = models.CharField(max_length=255, unique=True)
    access_token = models.CharField(max_length=255, editable=False)
    device_id = models.CharField(max_length=255, editable=False, default=uuid.uuid4)
    homeserver = models.CharField(max_length=255, default='matrix.org')
    display_name = models.CharField(max_length=255, null=True, blank=True)
    avatar_url = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.matrix_user_id

class SMUser(models.Model):
    display_name = models.CharField(max_length=255)
    matrix_user = models.ManyToManyField(MatrixUser)
    last_login_at = models.DateTimeField(auto_now=True)
    custom_pref = models.JSONField()
    photos = models.ManyToManyField(Photos)
    videos_long = models.ManyToManyField(LongVideo)
    videos_short = models.ManyToManyField(ShortVideo)
    audio = models.ManyToManyField(Audio)
    music = models.ManyToManyField(Music)
    project = models.ManyToManyField(Project)

    def __str__(self):
        return self.display_name