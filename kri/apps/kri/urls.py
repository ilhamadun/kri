"""URL configuration for kri app."""

from django.conf.urls import url
from . import views

app_name = 'kri'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
