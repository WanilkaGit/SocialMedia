from django.db import models

# Create your models here.
class ShortVideo(models.Model):#for shorts type video
    short_video = models.FileField()
    size = models.CharField(max_length=60)
    long = models.CharField(max_length=60)
    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(null=True, blank=True)

    share_link = models.TextField()
    share_title = models.CharField(max_length=255)

class LongVideo(models.Model):#fro usually video type
    long_video = models.FileField()
    size = models.CharField(max_length=60)
    long = models.CharField(max_length=60)
    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    share_link = models.TextField()
    share_title = models.CharField(max_length=255)

class TemplateVideo(models.Model):#fro usually video type
    long_video = models.FileField()
    size = models.CharField(max_length=60)
    long = models.CharField(max_length=60)
    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    share_link = models.TextField()
    share_title = models.CharField(max_length=255)

class ShortVideoComments(models.Model):
    video = models.ManyToManyField((ShortVideo, LongVideo, TemplateVideo), related_name="comments")
    text = models.TextField()
    author = models.CharField()
    # likes = models.TextChoices()

class LongVideoComments(models.Model):
    video = models.ManyToManyField((ShortVideo, LongVideo, TemplateVideo), related_name="comments")
    text = models.TextField()
    author = models.CharField()
    # likes = models.TextChoices()

class TemplateVideoComments(models.Model):
    video = models.ManyToManyField((ShortVideo, LongVideo, TemplateVideo), related_name="comments")
    text = models.TextField()
    author = models.CharField()
    # likes = models.TextChoices()