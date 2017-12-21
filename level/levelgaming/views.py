from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm, VideoForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
# from .tokens import account_activation_token
from django.core.mail import EmailMessage
import datetime
import levelgaming.esports_news_test as es


# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        #newsstories = es.getNews("a9f1a681-546e-43b1-96aa-24443c47a837")
        newsstories = ["l","p"]
        jews = list(User.objects.values('username'))
        jews = [j["username"] for j in jews]
        print(jews)
        return render(request, 'index.html', {"newsstories":newsstories,"users":jews})

class ProfileView(TemplateView):
    def get(self, request, **kwargs):
        followers = request.user.profile.followers
        followers = (json.loads(followers))
        followers = followers["followers"]
        following = request.user.profile.following
        following = (json.loads(following))
        following = following["following"]
        return render(request, 'profile.html',{"followers":followers,"following":following})

def addvideo(request):
    form = VideoForm(request.POST or None)
    if request.POST and form.is_valid():
        saveform = form.save(commit=False)
        saveform.link = form.cleaned_data.get('bannerurl')
        saveform.username = request.user.username
        saveform.save()
        return redirect("profile")
    return render(request, 'addvideo.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect('home')# Redirect to a success page.
    return render(request, 'login.html', {'form': form })

def logout_view(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect("home")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            saveform = form.save(commit=False)
            saveform.username = form.cleaned_data.get('username')
            saveform.save()
            user = User.objects.get(username=form.cleaned_data.get('username'))
            dic = {}
            dic["followers"] = ["test","whatever"]
            followingdic = {}
            followingdic["following"] = ["jim","john","jack"]
            user.profile.followers = json.dumps(dic)
            user.profile.following = json.dumps(followingdic)
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
