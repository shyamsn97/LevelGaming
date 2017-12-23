from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm, VideoForm, VideoSearch
from .models import Video
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
# from .tokens import account_activation_token
from django.core.mail import EmailMessage
import datetime, pytz
import levelgaming.esports_news_test as es        
import lxml
import urllib.request
from lxml import etree


# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        #newsstories = es.getNews("a9f1a681-546e-43b1-96aa-24443c47a837")
        newsstories = ["l","p"]
        jews = list(User.objects.values('username'))
        jews = [j["username"] for j in jews]
        print(jews)
        return render(request, 'index.html', {"newsstories":newsstories,"users":jews})

def videos_view(request):
    # def get(self, request, **kwargs):
        form = VideoSearch(request.POST or None)
        if request.POST and form.is_valid():
            videolist = list(Video.objects.values_list('link',flat=True).filter(username=form.cleaned_data.get('search')).order_by('username'))
            videotitles = list(Video.objects.values_list('title',flat=True).filter(username=form.cleaned_data.get('search')).order_by('username'))
            videousers = list(Video.objects.values_list('username',flat=True).filter(username=form.cleaned_data.get('search')).order_by('username'))
            tag = "Videos by User: " + form.cleaned_data.get('search')
        else:
            videolist = list(Video.objects.values_list('link',flat=True).order_by('-date')[:10])
            videotitles = list(Video.objects.values_list('title',flat=True).order_by('-date')[:10])
            videousers = list(Video.objects.values_list('username',flat=True).order_by('-date')[:10])
            tag = "Recent Videos"
        # videofull = list(zip(videolist, videotitles))
        # print(videofull)
        return render(request, 'videos.html',{"tag":tag,"form":form,"users":videousers,"videos":videolist,"videotitles":videotitles})

class ProfileView(TemplateView):
    def get(self, request, **kwargs):
        followers = request.user.profile.followers
        followers = (json.loads(followers))
        followers = followers["followers"]
        following = request.user.profile.following
        following = (json.loads(following))
        following = following["following"]
        videolist = list(Video.objects.values_list('link',flat=True).filter(username=request.user.username))
        videotitles = list(Video.objects.values_list('title',flat=True).filter(username=request.user.username))
        # videofull = list(zip(videolist, videotitles))
        # print(videofull)
        return render(request, 'profile.html',{"followers":followers,"following":following,"videos":videolist,"videotitles":videotitles})

def addvideo(request):
    form = VideoForm(request.POST or None)
    if request.POST and form.is_valid():
        saveform = form.save(commit=False)
        banner = form.cleaned_data.get('bannerurl')
        youtube = etree.HTML(urllib.request.urlopen(banner).read()) 
        video_title = youtube.xpath("//span[@id='eow-title']/@title")
        banner = banner.replace("watch?v=","embed/")
        saveform.link = banner
        saveform.username = request.user.username
        saveform.title = video_title[0]
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
