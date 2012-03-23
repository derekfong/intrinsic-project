from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('Student.views',
	url(r'^$', 'index'),
	url(r'^activities/$', 'activities'),
	url(r'^syllabus/$', 'syllabus'),
	url(r'^announcements/$', 'announcements'),
)
