from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'quiz.views.quizIndex'),
	url(r'^(?P<quiz_id>\d+)/$', 'quiz.views.view_Questions')

)
