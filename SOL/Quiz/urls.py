from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'quiz.views.quizIndex'),
	url(r'^(?P<answer_id>\d+)/submit/$', 'submit')
)
