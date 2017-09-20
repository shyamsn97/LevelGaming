
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from poppin.models import myUser as User
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
import json



class ProfileForm(ModelForm):
    first_names = forms.CharField(max_length=254, label="First Name")
    last_names = forms.CharField(max_length=254, label="Last Name")
    busyname = forms.CharField(max_length=254, label="Business Name")

    # def save(self, request):
    #     newuser = request.user
    #     data = self.cleaned_data
    #     diction = json.loads(request.user.content)
    #     diction['businessname'] = data['busyname']
    #     user = User(email=newuser.email,first_name=data['first_names'],
    #     last_name=data['last_names'],content=diction)
    #     user.update()
    #     return user

    class Meta:
        model = User
        fields = ('first_names','last_names','busyname',)

class LocationForm(ModelForm):
    address = forms.CharField(max_length=254)
    opentime = forms.CharField(max_length=254,label="Open Time")
    closetime = forms.CharField(max_length=254,label="Close Time")

    # def save(self, request):
    #     newuser = request.user
    #     data = self.cleaned_data
    #     diction = json.loads(request.user.content)
    #     diction['businessname'] = data['busyname']
    #     user = User(email=newuser.email,first_name=data['first_names'],
    #     last_name=data['last_names'],content=diction)
    #     user.update()
    #     return user

    class Meta:
        model = User
        fields = ('address','opentime','closetime',)

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user



class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    # last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    firstname = forms.CharField(max_length=254, label="First Name")
    lastname = forms.CharField(max_length=254, label="Last Name")
    businessname = forms.CharField(max_length=254, label="Business Name")
    address = forms.CharField(max_length=254)
    opentime = forms.DateTimeField(input_formats=['%H:%M'],label="Open Time")
    closetime = forms.DateTimeField(input_formats=['%H:%M'],label="Close Time")




    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'firstname', 'lastname', 'businessname', 'address', 'opentime','closetime',)
 
