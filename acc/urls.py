from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^register/$', views.register),
    url(r'^changeSet/$', views.change_user_setting),
    url(r'^changePass/$', views.change_user_pass),
    url(r'^eregister/$', views.eregister),
]
