
from django.conf.urls import patterns, url, include
import views

urlpatterns = [
    # url(r'', views.get_image, name='get_image'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^save/$', views.save, name='save'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^imagedetail/$', views.get_image, name='image'),
]