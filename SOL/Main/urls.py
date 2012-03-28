from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('Main.views',
	url(r'^$', 'index'),
	url(r'login/$', 'login_view'),
	url(r'logout/$', 'logout_view'),
	url(r'settings/$', 'setting'),
	url(r'settings/update/$', 'updateSetting'),
)
