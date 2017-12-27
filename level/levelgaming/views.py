from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.contrib import messages
import json
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm, VideoForm, VideoSearch
from .models import Video
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
import datetime
import levelgaming.esports_news_test as es        
import lxml
import urllib.request
from lxml import etree
from PIL import Image
from django import forms




# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        newsstories = es.getNews("a9f1a681-546e-43b1-96aa-24443c47a837")
        videolist = list(Video.objects.values_list('link',flat=True).order_by('-date'))
        videotitles = list(Video.objects.values_list('title',flat=True).order_by('-date'))
        videousers = list(Video.objects.values_list('username',flat=True).order_by('-date'))
      #  newsstories = ["l","p"]
        # jews = list(User.objects.values('username'))
        # jews = [j["username"] for j in jews]
        return render(request, 'index.html', {"newsstories":newsstories,"users":videousers,"videos":videolist,"videotitles":videotitles})

class ActivateStuff(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'activatestuff.html', context=None)


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

def usersearch(request):
        form = VideoSearch(request.POST or None)
        username = " "
        following = 99
        followers = 99
        tag = " "
        videotitles = []
        videolist = []
        videousers = []
        check = 0
        if request.POST and form.is_valid():
            try:
                user = User.objects.get(username=form.cleaned_data.get('search'))
                username = user.username
                #following = len(user.profile.following["following"])
                followers = user.profile.followers
                followers = (json.loads(followers))
                followers = len(followers["followers"])
                following = user.profile.following
                following = (json.loads(following))
                following = len(following["following"])
                #followers = len(user.profile.following["followers"])
                videolist = list(Video.objects.values_list('link',flat=True).filter(username=form.cleaned_data.get('search')).order_by('-date'))
                videotitles = list(Video.objects.values_list('title',flat=True).filter(username=form.cleaned_data.get('search')).order_by('-date'))
                videousers = list(Video.objects.values_list('username',flat=True).filter(username=form.cleaned_data.get('search')).order_by('-date'))
                tag = "Videos by User: " + form.cleaned_data.get('search')
            except Exception as e:
                tag = "User: " + form.cleaned_data.get("search") + " not found"        
        else:
            username = " "
        # videofull = list(zip(videolist, videotitles))
        # print(videofull)
        return render(request, 'usersearch.html',{"tag":tag, "check":check,"username":username,"following":following,"followers":followers,"form":form,"users":videousers,"videos":videolist,"videotitles":videotitles})

class ProfileView(TemplateView):
    def get(self, request, **kwargs):
        # profile_pic = request.user.profile.profile_pic
        # profile_pic = (json.loads(followers))
        followers   = request.user.profile.followers
        followers   = (json.loads(followers))
        followers   = followers["followers"]
        following   = request.user.profile.following
        following   = (json.loads(following))
        following   = following["following"]
        videolist   = list(Video.objects.values_list('link',flat=True).filter(username=request.user.username))
        videotitles = list(Video.objects.values_list('title',flat=True).filter(username=request.user.username))
        # videofull = list(zip(videolist, videotitles))
        # print(videofull)
        return render(request, 'profile.html',{"followers":followers,"following":following,"videos":videolist,"videotitles":videotitles})

def delete(request, vid):
    if "https://" in vid:
        vid = vid
    else:
        vid = vid.replace("https:/","https://")
    query = Video.objects.get(link__contains=vid)
    query.delete()
    return redirect("profile")

def follow(request, name):
    user = request.user
    otheruser = User.objects.get(username=name)
    following = request.user.profile.following
    following = (json.loads(following))
    if otheruser.username in following["following"]:
        print("already in list")
    else:
        following["following"].append(otheruser.username)
        print(following)
        user.profile.following = json.dumps(following)
        user.save()
        followers = otheruser.profile.followers
        followers = (json.loads(followers))
        followers["followers"].append(user.username)
        otheruser.profile.followers = json.dumps(followers)
        otheruser.save()
    return redirect("profile")

def linkprofile(request, name):
    user = User.objects.get(username=name)
    username = user.username
    check = 1
    #following = len(user.profile.following["following"])
    followers = user.profile.followers
    followers = (json.loads(followers))
    followers = len(followers["followers"])
    following = user.profile.following
    following = (json.loads(following))
    following = len(following["following"])
    #followers = len(user.profile.following["followers"])
    videolist = list(Video.objects.values_list('link',flat=True).filter(username=name).order_by('-date'))
    videotitles = list(Video.objects.values_list('title',flat=True).filter(username=name).order_by('-date'))
    videousers = list(Video.objects.values_list('username',flat=True).filter(username=name).order_by('-date'))
    tag = "Videos by User: " + name
    return render(request, 'usersearch.html',{"tag":tag,"check":check,"username":username,"following":following,"followers":followers,"users":videousers,"videos":videolist,"videotitles":videotitles})

def addvideo(request):
    form = VideoForm(request.POST or None)
    message = ""
    if request.POST and form.is_valid():
        saveform            = form.save(commit=False)
        message = ""
        banner              = form.cleaned_data.get('bannerurl')
        youtube             = etree.HTML(urllib.request.urlopen(banner).read()) 
        video_title         = youtube.xpath("//span[@id='eow-title']/@title")
        banner              = banner.replace("watch?v=","embed/")
        if Video.objects.filter(link=banner).exists():
            message = "Video already exists"
            return render(request, 'addvideo.html', {'form': VideoForm(),'message':message})
        else:
            saveform.link       = banner
            saveform.username   = request.user.username
            saveform.title      = video_title[0]
            saveform.save()
        return redirect("profile")
    return render(request, 'addvideo.html', {'form': form,'message':message})

#def addprofilepic(request):
#    form = ProfilePicForm(request.POST, request.FILES)
#    if request.POST and form.is_valid():
#        user = request.user
#        avatar = form.cleaned_data['avatar']
#        profile = user.get_profile()
#        profile.avatar = avatar
#        profile.save()
#    return render(request, 'addprofilepic.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user    = form.login(request)
        if user and user.is_active == True:
            login(request, user)
            return redirect('home')# Redirect to a success page.
    return render(request, 'login.html', {'form': form })

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("home")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('profile')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            saveform          = form.save(commit=False)
            saveform.username = form.cleaned_data.get('username')
            #saveform.is_active = False
            saveform.save()
            user             = User.objects.get(username=form.cleaned_data.get('username'))
            dic              = {}
            dic["followers"] = []
            followingdic     = {}
            followingdic["following"]   = []
            user.profile.followers      = json.dumps(dic)
            user.profile.following      = json.dumps(followingdic)
            #current_site = get_current_site(request)
            #print(current_site.domain)
            #message = render_to_string('acc_active_email.html', {
            #    'user':user,
            #    'domain':current_site.domain,
            #    'uid': urlsafe_base64_encode(force_bytes(user.id)),
            #    'token': account_activation_token.make_token(user),
            #})
            #mail_subject = 'Activate your account'
            #to_email = form.cleaned_data.get('email')
            #email = EmailMessage(mail_subject, message, to=[to_email])
            #email.send()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
