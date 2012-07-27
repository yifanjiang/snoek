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

    (r'^$', index),
    (r'^admin/', include(admin.site.urls)),

    # About page
    (r'^about/', about),

    # Activity
    (r'^activity/(\d+)$',           view_activity),
    (r'^edit_activity(\d+)$',       view_update_activity),
    (r'^edit_submit(\d+)$',         update_activity),
    (r'^new(.*)$',                  view_create_activity),
    (r'^activity_submit$',          create_activity),
    (r'^vote_submit(\d+)$',         save_vote_in_activity),
    (r'^deltact(\d+)$',             delt_activity),
    (r'^download_activity/(\d+)$',  download_activity),

    # Vote specific
    (r'^whovotewhat/(\d+)$',        view_votes_by_all_users),
    (r'^activity/(\d+)/vote/$',     take_vote),
    (r'^activity/(\d+)/revote/$',   take_revote),
    (r'^activity/(\d+)/delvote/$',  del_vote),

    # User management
    (r'^accounts/logout.*$',        'django.contrib.auth.views.logout'),
    (r'^accounts/login.*$',         'django.contrib.auth.views.login'),
    (r'^accounts/chpwd/$',          'django.contrib.auth.views.password_change', {'post_change_redirect': '/'}),



#    (r'^accounts/chpwd/$', 'django.contrib.auth.views.password_change_done'),
)

urlpatterns += patterns('snoek.meeting.views',
    # Meeting room
    (r'^meetingroom/$',                      'index'),
    (r'^meetingroom/showmeeting/$',          'show_meeting'),
    (r'^meetingroom/showevent/$',            'show_event'),
    (r'^meetingroom/getstatus/$',            'get_status'),
    (r'^meetingroom/booking/$',              'new_event'),
    (r'^meetingroom/set_event/$',            'set_event'),
    (r'^meetingroom/showstatus/$',           'show_status'),
    (r'^meetingroom/delevent_(\d+)/$',       'del_event'),
)

urlpatterns += patterns('',
    url(r'^library/',include('library.urls')),
)



if settings.DEBUG:
    urlpatterns += patterns("",
            (r"^media/(?P<path>.*)$","django.views.static.serve",{'document_root':settings.MEDIA_ROOT}),)
