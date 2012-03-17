from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('Instructor.views',
	url(r'^$', 'index'),
)
