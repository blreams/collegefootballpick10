from django.conf.urls import patterns, url
from pick10 import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home, name='home'),
)
