from django import forms
from django.conf import settings

class RegistrationForm(forms.Form):
    password = forms.CharField(
        label='Пароль:',
        widget=forms.PasswordInput(),
        required=True,
        min_length=8,
        error_messages={'required': 'Це поле обов\'язкове.'}
    )
    display_name = forms.CharField(
        label='Відображуване ім\'я (необов\'язково):',
        required=False
    )

class LoginForm(forms.Form):
    password = forms.CharField(
        label='Пароль:',
        widget=forms.PasswordInput(),
        required=True
    )