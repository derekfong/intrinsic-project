from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('Student.views',
	url(r'^$', 'index'),
	url(r'^activities/$', 'activities'),
	url(r'^activities/(?P<aid>\d+)/submission/$', 'activities_submit'),
	url(r'^syllabus/$', 'syllabus'),
	url(r'^syllabus/download/$', 'downloadSyllabus'),
	url(r'^announcements/$', 'announcements'),
	url(r'^slides/$', 'slides'),
	url(r'^quiz/$', 'quiz'),
	url(r'^quiz/(?P<qid>\d+)/$', 'quizTake'),
	url(r'^quiz/results/(?P<qid>\d+)/$', 'quizResults'),
	url(r'^forum/', include('Forum.urls')),
)
