from django.db import models

# Create your models here.
class Lessons(models.Model):
    lesson_file = models.FileField()
    lesson_title = models.CharField(max_length=255)
    lesson_description = models.TextField()
    lesson_time = models.TimeField()
    lc_id = models.IntegerField()


class Cources(models.Model):
    c_type = models.Choices()
    c_title = models.CharField(max_length=255)
    c_description = models.TextField()
    c_prize = models.IntegerField()
    c_addeting_files = models.BooleanField(default=False)
    c_uploaded = models.DateTimeField(auto_now_add=True)
    c_lessons = models.OneToOneField(to=Lessons, related_name="cource")
    c_files = models.models.FileField()
    c_rating = models.IntegerField()
    c_bye_count = models.IntegerField()
    pay_choices = models.Choices()