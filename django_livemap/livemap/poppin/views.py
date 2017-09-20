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
    editprofileform = ProfileForm(data=request.POST, instance=request.user, initial={'first_names': dictionary["firstname"], 
            'last_names': dictionary["lastname"], 'busyname': dictionary["businessname"]})
    editlocationform = LocationForm(data=request.POST, instance=request.user, initial={'address': dictionary["locations"][0]["address"], 
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
# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = authenticate(email=email,password=form.cleaned_data.get('password1'))
#             login(request, user)
#             return redirect('home')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})

# def edit_profile(request):

#     if 'edit_button' in request.POST:
#              form = ProfileForm(request.POST)
#              f_user = User.objects.get(username=request.user.id)
#              f_profile_name = form.cleaned_data['profile_name']
#              p = UserProfile(user=f_user, profile_name=f_profile_name)
#              p.save()
#     else:
#             form = ProfileForm()
#     return render_to_response('userprofile_template.html', locals(), context_instance=RequestContext(request))
    

# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/home/')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()

#     return render(request, '/home/', {'form': form})