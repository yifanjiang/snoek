from django.conf.urls.defaults import *
from snoek.activities.views import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^snoek/', include('snoek.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^$', index),                                              
    (r'^activity/(\d+)$', view),
    (r'^whovotewhat/(\d+)$', view_by_all_users),
    (r'^download_activity/(\d+)$', download_activity),
    (r'^activity/(\d+)/vote/$', vote),                       
    (r'^accounts/logout.*$', 'django.contrib.auth.views.logout'),
    (r'^accounts/login.*$', 'django.contrib.auth.views.login'),
    (r'^accounts/chpwd/$', 'django.contrib.auth.views.password_change', {'post_change_redirect': '/'}),
#    (r'^accounts/chpwd/$', 'django.contrib.auth.views.password_change_done'),
)
