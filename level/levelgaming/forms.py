
from django import forms
from django.forms import ModelForm
from .models import Video
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import json


class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return password

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class VideoForm(ModelForm):
    bannerurl = forms.URLField(max_length=250,label="Link")
    class Meta:
        model = Video
        fields = ['bannerurl']