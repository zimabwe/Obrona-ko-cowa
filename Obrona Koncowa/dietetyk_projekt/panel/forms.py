from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class PacjentRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Wprowadź prawidłowy adres e-mail.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PacjentLoginForm(AuthenticationForm):

    pass