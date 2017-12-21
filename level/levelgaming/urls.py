
from django.conf.urls import include
from django.conf.urls import url
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import logout, login
from levelgaming import views as levelgaming_views


urlpatterns = [
    url(r'^$', levelgaming_views.HomePageView.as_view(), name='home'),
    url(r'^profile/$', levelgaming_views.ProfileView.as_view(), name='profile'),
    url(r'^signup/$', levelgaming_views.signup, name='signup'),
    url(r'^addvideo/$', levelgaming_views.addvideo, name='addvideo'),
    url(r'^login/$', levelgaming_views.login_view, name='login'),
    url(r'^logout/$', levelgaming_views.logout_view, name='logout'),
] 
