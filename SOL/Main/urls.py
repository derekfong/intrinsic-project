from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout, password_change, password_reset, password_reset_confirm, password_reset_done, password_reset_complete
from Student.views import getClassList

urlpatterns = patterns('Main.views',
	url(r'^$', 'index'),
	url(r'login/$', 'login_view'),
	url(r'logout/$', 'logout_view'),
	url(r'password/change/$', password_change, {'post_change_redirect': '/accounts/settings/'}),
	#url(r'password/reset/$', password_reset,  {'from_email': 'itsatme@gmail.com', }),
	#url(r'password/reset/done/$', password_reset_done),
	#url(r'password/reset/confirm/$', password_reset_confirm,  {'post_reset_redirect:': '/', 'from_email': 'itsatme@gmail.com', }),
	url(r'^password/reset/$', password_reset, {'post_reset_redirect' : '/accounts/password/reset/done/'}),
	url(r'^password/reset/done/$', password_reset_done),
	url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'post_reset_redirect' : '/accounts/password/done/'}),
	url(r'^password/done/$', password_reset_complete),
	url(r'settings/$', 'setting'),
	url(r'settings/update/$', 'updateSetting'),
)
