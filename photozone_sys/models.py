from django.db import models

# Create your models here.
class Photos(models.Model):
    photos = models.FileField()
    size = models.CharField(max_length=60)
    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    share_link = models.TextField()
    share_title = models.CharField(max_length=255)

class Imgs4Designs(models.Model):
    images = models.FileField()
    size = models.CharField(max_length=60)
    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    share_link = models.TextField()
    share_title = models.CharField(max_length=255)

class PhotosComments(models.Model):
    photo = models.ManyToManyField(Photos, related_name="comments")
    text = models.TextField()
    author = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)

class Imgs4DesignsComments(models.Model):
    image = models.ManyToManyField(Imgs4Designs, related_name="comments")
    text = models.TextField()
    author = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)
