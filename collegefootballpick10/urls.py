from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='admin_password_reset_done'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^$', 'pick10.views.index', name='index'),
    url(r'^pick10/', include('pick10.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
