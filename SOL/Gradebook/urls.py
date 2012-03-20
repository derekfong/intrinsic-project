from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('Gradebook.views',
	url(r'^$', 'index'),
	url(r'^(?P<aid>\d+)', 'viewGrade'),
)
