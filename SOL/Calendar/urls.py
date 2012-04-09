from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('Calendar.views',
	url(r'^$', 'index'),
	url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'day_events'),
	url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<eid>\d+)/$', 'update_event'),
	url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<eid>\d+)/remove/$', 'remove_event'),
	url(r'^event/$', 'event'),
	url(r'^event/label/$', 'label'),
	url(r'^event/label/(?P<lid>\d+)/$', 'update_label'),
)
