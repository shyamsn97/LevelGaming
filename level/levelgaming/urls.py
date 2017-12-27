from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth import views as auth_view
#from django.contrib.auth.views import logout, login
from levelgaming import views as levelgaming_views


urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^$', levelgaming_views.HomePageView.as_view(), name='home'),
    url(r'^profile/$', levelgaming_views.ProfileView.as_view(), name='profile'),
    url(r'^videos/$', levelgaming_views.videos_view, name='videos'),
    url(r'^usersearch/$', levelgaming_views.usersearch, name='usersearch'),
    url(r'^signup/$', levelgaming_views.signup, name='signup'),
    url(r'^addvideo/$', levelgaming_views.addvideo, name='addvideo'),
#    url(r'^addprofilepic/$', levelgaming_views.addprofilepic, name='addprofilepic'),
    url(r'^login/$', levelgaming_views.login_view, name='login'),
    url(r'^logout/$', levelgaming_views.logout_view, name='logout'),
    url(r'^delete/(?P<vid>.*)$', levelgaming_views.delete, name='delete-vid'),
    url(r'^follow/(?P<name>.*)$', levelgaming_views.follow, name='follow'),
    url(r'^linkprofile/(?P<name>.*)$', levelgaming_views.linkprofile, name='linkprofile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        levelgaming_views.activate, name='activate'), 
    url(r'^activatestuff/$', levelgaming_views.ActivateStuff.as_view(), name='activatestuff'),
] 
