
from django.conf.urls import patterns, url, include
import views

urlpatterns = [
    url(r'^edit/$', views.edit, name='edit'),
    url(r'', views.get_image, name='get_image'),
]