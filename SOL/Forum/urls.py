from django.conf.urls.defaults import patterns, include, url
from board.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('board.views',
	url(r'^$', 'topic_display'),
	url(r'^(?P<topic_id>\d+)/$', 'message_display'),

)
