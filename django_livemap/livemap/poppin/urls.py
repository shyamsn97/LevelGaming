
from django.conf.urls import include
from django.conf.urls import url
from poppin import views
from poppin import views as poppin_views
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import logout, login

urlpatterns = [
    url(r'^$', poppin_views.HomePageView.as_view(), name='home'),
    # url(r'^profile/$', poppin_views.showprofile, name='profile'),
	url(r'^profile/$', poppin_views.editprofile, name='profile'),
	url(r'^makelocation/$', poppin_views.location_view, name='makelocation'),
    # url(r'^login$', auth_view.login, {'template_name': 'login.html'}, name='login'),
    url(r'^login/$', poppin_views.login_view, name='login'),
    url(r'^signup/$', poppin_views.signup, name='signup'),
    url(r'^logout$', poppin_views.logout_view, name='logout'),
]
