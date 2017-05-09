"""URL configuration for participant application."""

from django.conf.urls import url
from . import views

app_name = 'attendance'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^monitor/$', views.monitor, name='monitor')
]
