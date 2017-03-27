"""URL configuration for participant application."""

from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'participant'

urlpatterns = [
    url(r'^login/', auth_views.login, {'template_name': 'participant/login.html'}, name='login'),
    url(r'^logout/', auth_views.logout_then_login, name='logout'),
]
