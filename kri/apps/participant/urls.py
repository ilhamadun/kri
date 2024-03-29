"""URL configuration for participant application."""

from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'participant'

authurls = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', auth_views.logout_then_login, name='logout'),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^team/krai/$', views.krai, name='krai'),
    url(r'^team/krsbi-beroda/$', views.krsbi_beroda, name='krsbi-beroda'),
    url(r'^team/krsti/$', views.krsti, name='krsti'),
    url(r'^team/krpai/$', views.krpai, name='krpai'),

    url(r'^person/(?P<person_type>[\w-]+)/$', views.person, name='person'),

    url(r'^tiket/$', views.supporter, name='supporter'),
    url(r'^tiket/verifikasi/([0-9]+)/$', views.verify_supporter, name='verify-supporter'),

] + authurls
