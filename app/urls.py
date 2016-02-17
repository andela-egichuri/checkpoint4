
from django.conf.urls import patterns, url, include
import views

urlpatterns = [
    url(r'^edit/$', views.edit, name='edit'),
]