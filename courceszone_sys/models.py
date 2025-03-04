from django.db import models

# Create your models here.
class Lessons(models.Model):
    l_file = models.FileField()
    l_title = models.CharField(max_length=255)
    l_description = models.TextField()
    l_time = models.TimeField()
    lc_id = models.IntegerField()

class Cources(models.Model):
    c_title = models.CharField(max_length=255)
    c_description = models.TextField()
    TYPE_CHOICES = [
        ("Audio", "audio"),
        ("Video", "video"),
        ("Photos", "photos"),
        ("3D Models", "3d-models"),
        ("Code", "code"),
        ("Finance", "finance"),
        ("Cryptography", "cryptography"),
        ("Science", "science"),
    ]
    c_type = models.CharField(choices=TYPE_CHOICES, default="code", max_length=20)
    c_prize = models.IntegerField()
    c_addeting_files = models.BooleanField(default=False)
    c_uploaded = models.DateTimeField(auto_now_add=True)
    c_lessons = models.ManyToManyField(to=Lessons, related_name="cources")
    c_files = models.CharField(max_length=300)
    c_rating = models.IntegerField(default=0)
    c_bye_count = models.IntegerField(default=0)
    PAY_CHOICES = [
        ("IBAN", "iban"),
        ("Card number", "card_number"),
    ]
    c_pay_choices = models.CharField(max_length=15, choices=PAY_CHOICES, default="card_number")