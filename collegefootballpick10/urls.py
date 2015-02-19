from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'pick10.views.home', name='home'),
    url(r'^pick10/', include('pick10.urls')),

    url(r'', include('django_browserid.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
