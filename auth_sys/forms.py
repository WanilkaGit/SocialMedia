from django import forms
from django.conf import settings

class RegistrationForm(forms.Form):
    matrix_user_id = forms.CharField(
        label='Matrix ID (@username:matrix.org):',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'pattern': '^@[a-zA-Z0-9._=-]+:matrix\\.org$',
            'title': 'Формат: @username:matrix.org',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Пароль:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        min_length=8,
        help_text='Пароль повинен містити мінімум 8 символів'
    )
    password_confirm = forms.CharField(
        label='Підтвердження пароля:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    display_name = forms.CharField(
        label='Відображуване ім\'я:',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Паролі не співпадають')
        
        return cleaned_data

class LoginForm(forms.Form):
    matrix_user_id = forms.CharField(
        label='Matrix ID (@username:matrix.org):',
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'pattern': '^@[a-zA-Z0-9._=-]+:matrix\\.org$',
            'title': 'Формат: @username:matrix.org',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Пароль:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def clean_matrix_user_id(self):
        matrix_user_id = self.cleaned_data.get('matrix_user_id')
        if not matrix_user_id.startswith('@') or not matrix_user_id.endswith(':matrix.org'):
            raise forms.ValidationError('Невірний формат Matrix ID. Приклад: @username:matrix.org')
        return matrix_user_id