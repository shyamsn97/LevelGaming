from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
import json
# from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from poppin.models import myUser
from .forms import SignUpForm, LoginForm, ProfileForm, LocationForm

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

    # def get(self, request, **kwargs):
    #     return render(request, 'profile.html', context=None)


def editprofile(request):
    dictionary = json.loads(request.user.content)
    editprofileform = ProfileForm(request.POST, instance=request.user, initial={'first_names': dictionary["firstname"], 
            'last_names': dictionary["lastname"], 'busyname': dictionary["businessname"]})
    editlocationform = LocationForm(request.POST, instance=request.user, initial={'address': dictionary["locations"][0]["address"], 
            'opentime': dictionary["locations"][0]["opentime"], 'closetime': dictionary["locations"][0]["closetime"]})
    templatelocations = dictionary["locations"]
    count = 0
    if request.method == 'POST':
        if editprofileform.is_valid():
            saveuser = editprofileform.save(commit=False)
            dictionary["businessname"] = editprofileform.cleaned_data.get('busyname')
            dictionary["firstname"] = editprofileform.cleaned_data.get('first_names')
            dictionary["lastname"] = editprofileform.cleaned_data.get('last_names')
            saveuser.content = json.dumps(dictionary)
            saveuser.save()
            return redirect('profile')

        if editlocationform.is_valid():
            saveuser = editlocationform.save(commit=False)
            dictionary["locations"][0]["address"] = editlocationform.cleaned_data.get('address')
            dictionary["locations"][0]["opentime"] = editlocationform.cleaned_data.get('opentime')
            dictionary["locations"][0]["closetime"] = editlocationform.cleaned_data.get('closetime')
            saveuser.content = json.dumps(dictionary)
            saveuser.save()
            formarray = [editlocationform]
            return redirect('profile')

    else:
        editprofileform = ProfileForm(request.POST or None, instance=request.user, initial={'first_names': dictionary["firstname"], 
            'last_names': dictionary["lastname"], 'busyname': dictionary["businessname"]})
        editlocationform = LocationForm(request.POST or None, instance=request.user, initial={'address': dictionary["locations"][0]["address"], 
            'opentime': dictionary["locations"][0]["opentime"], 'closetime': dictionary["locations"][0]["closetime"]})
        formarray = [editlocationform]        
    return render(request, 'profile.html', {'formarray': formarray, 'locations': templatelocations,'profileform': editprofileform, 'locationform': editlocationform,
        'dictionary': dictionary})

def signup(request):
    desired_format = '%H:%M'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            saveform = form.save(commit=False)
            saveform.first_name = form.cleaned_data.get('firstname')
            saveform.last_name = form.cleaned_data.get('lastname')
            location = {'address':form.cleaned_data.get('address'),'opentime':form.cleaned_data.get('opentime').strftime(desired_format),
            'closetime':form.cleaned_data.get('closetime').strftime(desired_format)}
            locationlist = [location]
            # jsonlist = json.dumps(locationlist)
            json_object = {'firstname': form.cleaned_data.get('firstname'),'lastname': form.cleaned_data.get('lastname'),
            'businessname': form.cleaned_data.get('businessname'), 'locations':locationlist}
            saveform.content = json.dumps(json_object)
            saveform.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

#@login_required
def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect("home")


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect('profile')# Redirect to a success page.
    return render(request, 'login.html', {'form': form })

def location_view(request):
    dictionary = json.loads(request.user.content)
    desired_format = '%H:%M'
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=request.user)
        if form.is_valid():
            saveform = form.save(commit=False)
            location = {'address':form.cleaned_data.get('address'),'opentime':form.cleaned_data.get('opentime'),
            'closetime':form.cleaned_data.get('closetime')}
            dictionary = json.loads(request.user.content)
            templatelocations = dictionary["locations"]
            templatelocations.append(location)
            dictionary["locations"] = templatelocations
            saveform.content = json.dumps(dictionary)
            saveform.save()
            return redirect('profile')
    else:
        form = LocationForm()
    return render(request, 'makelocation.html', {'form': form })
