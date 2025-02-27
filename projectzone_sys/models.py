from django.db import models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    share_link = models.TextField()
    share_title = models.CharField(max_length=255)

class ProjectFile(models.Model):
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE)
    file = models.FileField()
    size = models.CharField(max_length=60)


class ProjectsComments(models.Model):
    project = models.ManyToManyField(Project, related_name="comments")
    text = models.TextField()
    author = models.CharField(max_length=255)
    likes = models.IntegerField(default=0)
    # likes = models.TextChoices()
