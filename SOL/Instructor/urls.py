from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('Instructor.views',
	url(r'^$', 'index'),
	url(r'^edit', 'greeting'),
	url(r'^syllabus/$', 'syllabus'),
	url(r'^syllabus/update/(?P<sid>\d+)$', 'updateSyllabus'),
	url(r'^activity/(?P<aid>\d+)/remove$', 'removeActivity'),
	url(r'^activity/(?P<aid>\d+)/submissions$', 'getSubmissions'),
	url(r'^activity/(?P<aid>\d+)$', 'updateActivity'),
	url(r'^activity/$', 'activity'),
	url(r'^announcement/(?P<anid>\d+)/remove$', 'removeAnnouncement'),
	url(r'^announcement/(?P<anid>\d+)$', 'updateAnnouncement'),
	url(r'^announcement/$', 'announcement'),
	url(r'^roster/$', 'roster'),
	url(r'^grades/$', 'grades'),
	url(r'^grades/file/$', 'grades_files'),
	url(r'^grades/form/$', 'grades_form'),
	url(r'^grades/form/(?P<aid>\d+)$', 'grades_input'),
	url(r'^slides/$', 'slides'),
	url(r'^slides/(?P<slid>\d+)/update$', 'updateSlides'),
	url(r'^slides/(?P<slid>\d+)/remove$', 'removeSlides'),
)
