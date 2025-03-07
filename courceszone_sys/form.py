from django import forms
from .models import Lessons, Cources


class CreatCourceForm():
    c_title = forms.CharField(max_length=255)
    c_description = forms
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
    c_type = forms.CharField(choices=TYPE_CHOICES, default="code", max_length=20)
    c_addeting_files = forms.BooleanField()
    c_files = forms.CharField(max_length=300)
    PAY_CHOICES = [
        ("IBAN", "iban"),
        ("Card number", "card_number"),
    ]
    c_pay_choices = forms.CharField(max_length=15, choices=PAY_CHOICES, default="card_number")