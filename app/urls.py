
from django.conf.urls import patterns, url, include
from app.views import edit, save, delete, get_image

urlpatterns = [
    url(r'^edit/$', edit, name='edit'),
    url(r'^save/$', save, name='save'),
    url(r'^delete/$', delete, name='delete'),
    url(r'^imagedetail/$', get_image, name='image'),
]