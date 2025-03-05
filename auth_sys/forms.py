from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import SMUser

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = SMUser
        fields = (UserCreationForm().Meta.fields + ("email", "username", "authentificator"))


    login = forms.CharField(
        max_length=255,
        label="Login",
        required=True,
        help_text="User login: User Name",
        widget=forms.TextInput()
    )
    authentificator = forms.CharField(
        max_length=255,
        label="authentificator",
        required=False,
        help_text="authentificator: user_name (except spaces)",
        widget=forms.TextInput()
    )
    email = forms.EmailField(
        max_length=255,
        label="Email",
        required=True,
        help_text="Email: someemail@gmail.com",
        widget=forms.EmailInput()
    )
    password1 = forms.CharField(
        max_length=255,
        label="Password1",
        required=True,
        help_text="Password: 12345678 (min symbols: 8)",
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        max_length=255,
        label="Password2",
        required=True,
        help_text="Password: 12345678 (min symbols: 8)",
        widget=forms.PasswordInput()
    )


    def clean_authentificator(self):
        authentificator = self.cleaned_data.get("authentificator")
        if " " in authentificator:
            raise forms.ValidationError("authentificator cannot contain spaces.")
        return authentificator

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class LoginForm(AuthenticationForm):
    authentificator = forms.CharField(
        max_length=255,
        label="authentificator",
        required=True,
        help_text="authentificator:",
        widget=forms.TextInput()
    )
    password = forms.CharField(
        max_length=255,
        label="Password",
        required=True,
        help_text="Enter your password",
        widget=forms.PasswordInput()
    )