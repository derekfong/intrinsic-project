from django.conf.urls.defaults import patterns, include, url
from Forum.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('Forum.views',
	url(r'^$', 'topic_display'),
	url(r'^(?P<topic_id>\d+)/$', 'message_display'),
	url(r'^(?P<topic_id>\d+)/delete/$', 'remove_topic'),
<<<<<<< HEAD
=======
	url(r'^(?P<topic_id>\d+)/(?P<msg_id>\d+)/delete/$', 'remove_post'),

>>>>>>> 0ff23bd7a9fb65b84f6bbe5022acd0e5a3ab3e87
)
