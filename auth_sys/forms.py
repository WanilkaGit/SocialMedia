from django import forms
from django.conf import settings

class RegistrationForm(forms.Form):
    matrix_user_id = forms.CharField(
        label='Matrix ID (@username:matrix.org):',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'pattern': '^@[a-zA-Z0-9._=-]+:matrix\\.org$', 'title': 'Формат: @username:matrix.org'})
    )
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
    matrix_user_id = forms.CharField(
        label='Matrix ID (@username:matrix.org):',
        max_length=255,
        required=True
    )
    password = forms.CharField(
        label='Пароль:',
        widget=forms.PasswordInput(),
        required=True
    )
