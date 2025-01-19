from django.db import models

# Create your models here.
class Audio(models.Model):
    audio = models.FileField()
    size = models.CharField(max_length=60)
    long = models.CharField(max_length=60)
    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    share_link = models.TextField()
    share_title = models.CharField(max_length=255)

class Music(models.Model):
    music = models.FileField()
    size = models.CharField(max_length=60)
    long = models.CharField(max_length=60)
    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    share_link = models.TextField()
    share_title = models.CharField(max_length=255)