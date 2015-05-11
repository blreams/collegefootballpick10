from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'pick10.views.index', name='index'),
    url(r'^pick10/', include('pick10.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)
