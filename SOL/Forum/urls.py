from django.conf.urls.defaults import patterns, include, url
from Forum.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('Forum.views',
	url(r'^$', 'topic_display'),
	url(r'^(?P<topic_id>\d+)/$', 'message_display'),
	url(r'^(?P<topic_id>\d+)/delete/$', 'remove_topic'),
	url(r'^(?P<topic_id>\d+)/(?P<msg_id>\d+)/delete/$', 'remove_post'),

)
