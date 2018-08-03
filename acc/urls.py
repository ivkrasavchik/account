from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
]