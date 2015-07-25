from django.conf.urls import patterns, url
from pick10 import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week_number>[0-9]{1,2})/results$', views.week_results, name='week_results'),
)
