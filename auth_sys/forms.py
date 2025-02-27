from django import forms
from django.conf import settings


class RegistrationForm(forms.Form):
    login
    email
    password1
    password2