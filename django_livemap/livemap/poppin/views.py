from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
import json
# from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect

from .forms import SignUpForm, LoginForm, ProfileForm

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

    # def get(self, request, **kwargs):
    #     return render(request, 'profile.html', context=None)


def editprofile(request):
    choice = 1
    dictionary = json.loads(request.user.content)
    if request.method == 'POST':
        editprofileform = ProfileForm(request.POST or None, initial={'first_names': request.user.first_name, 
            'last_names': request.user.last_name, 'busyname': disctionary["businessname"]})
        saveprofile = editprofileform.save(commit=False)
        dictionary["businessname"] = form.cleaned_data.get('busyname')
        saveprofile.content = json.dumps(dictionary)
        saveform.first_name = form.cleaned_data.get('firstname')
        saveform.last_name = form.cleaned_data.get('lastname')
        saveform.save()
        return redirect('profile')
    else:
        editsaveform = ProfileForm(request.POST or None, initial={'first_names': request.user.first_name, 
            'last_names': request.user.last_name, 'busyname': dictionary["businessname"]})
    return render(request, 'profile.html', {'form': editsaveform, 'choice': choice})


def showprofile(request):
    dictionary = json.loads(request.user.content)
    return render(request, 'profile.html', {'dictionary': dictionary})
        
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            saveform = form.save(commit=False)
            saveform.first_name = form.cleaned_data.get('firstname')
            saveform.last_name = form.cleaned_data.get('lastname')
            json_object = {'firstname': form.cleaned_data.get('firstname'),'lastname': form.cleaned_data.get('lastname'),
            'businessname': form.cleaned_data.get('businessname'),'address': form.cleaned_data.get('address'),
            'cardcompany': form.cleaned_data.get('cardcompany'), 'accountnumber': form.cleaned_data.get('accountnumber')}
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