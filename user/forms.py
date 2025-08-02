from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class MyUserRegisterForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('email', 'username')


class MyUserLoginForm(forms.Form):
    email = forms.EmailField(label='Почта')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')