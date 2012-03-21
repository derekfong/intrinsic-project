from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('Instructor.views',
	url(r'^$', 'index'),
	url(r'^syllabus/$', 'syllabus'),
	url(r'^activity/(?P<aid>\d+)/remove$', 'removeActivity'),
	url(r'^activity/(?P<aid>\d+)$', 'updateActivity'),
	url(r'^activity/$', 'activity'),
	url(r'^announcement/(?P<anid>\d+)/remove$', 'removeAnnouncement'),
	url(r'^announcement/(?P<anid>\d+)$', 'updateAnnouncement'),
	url(r'^announcement/$', 'announcement'),
	url(r'^grades/$', 'grades'),
)