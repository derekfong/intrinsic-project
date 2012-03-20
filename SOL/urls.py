from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', include('Main.urls')),

	(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/csmadmin/tools/jquery'}),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

	url(r'^accounts/', include('Main.urls')),
	
	url(r'^course/(?P<department>[a-zA-z]+)/(?P<class_number>\d+)/(?P<year>\d+)/(?P<semester>[a-zA-z]+)/(?P<section>[a-zA-z]\d{3})/instructor/', include('Instructor.urls')),
	
	url(r'^course/(?P<department>[a-zA-z]+)/(?P<class_number>\d+)/(?P<year>\d+)/(?P<semester>[a-zA-z]+)/(?P<section>[a-zA-z]\d{3})/grades/', include('Gradebook.urls')),
		
	url(r'^course/(?P<department>[a-zA-z]+)/(?P<class_number>\d+)/(?P<year>\d+)/(?P<semester>[a-zA-z]+)/(?P<section>[a-zA-z]\d{3})/', include('Student.urls')),


)
