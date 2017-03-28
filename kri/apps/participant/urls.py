"""URL configuration for participant application."""

from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'participant'

authurls = [
    url(r'^login$', auth_views.login, {'template_name': 'participant/login.html'}, name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^krai/$', views.krai, name='krai'),
    url(r'^krsbi-beroda/$', views.krsbi_beroda, name='krsbi-beroda'),
    url(r'^krsti/$', views.krsti, name='krsti'),
    url(r'^krpai/$', views.krpai, name='krpai'),
    
] + authurls
