from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Form(UserCreationForm):
    """Form for the image model"""

    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['username','password1','password2']