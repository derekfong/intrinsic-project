from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from Main.models import Course, Setting, ClassList
from datetime import date
from Instructor.forms import SettingForm
from Instructor.models import Announcement
from django.contrib.auth import authenticate, login
import datetime
from datetime import timedelta

#This is just for the index page when user first reaches website


# Create your views here.
def index(request):
	user = request.user
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester).order_by('department', 'class_number')
	old_class_list = Course.objects.filter(classlist__uid=user.id, year__lt=year).order_by('-year', 'department', 'class_number')
		
	content={'class_list': class_list, 'old_class_list': old_class_list, 'globalAnnouncements': getGlobalAnnouncements(user)}
	return render_to_response('main/index.html', content,
			context_instance=RequestContext(request))

def login_view(request):
	if request.method == 'POST':
   		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(request, user)
			return HttpResponseRedirect( '/' )
		else:
			message = 'Please enter the correct username and password.'
			return render_to_response('main/index.html', { 'message': message, },
				context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect( '/' )

def logout_view(request):
	auth.logout(request)
	return HttpResponseRedirect("/")
	
def setting(request):
	# settings option for user in nav bar
	user = request.user
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester).order_by('department', 'class_number')
	
	message = ''
	if request.method == 'POST':
		setting = Setting(uid=user.userprofile)
		form = SettingForm(request.POST, instance=setting)
		if form.is_valid():
			form.save()
			message = 'You have succcessfully updated your settings.'
	else:
		try:
			setting = Setting.objects.get(uid=user.id)
			return HttpResponseRedirect("/accounts/settings/update/")
		except Setting.DoesNotExist:
			form = SettingForm()
		
	content = {'class_list': class_list, 'form': form, 'message': message, 'globalAnnouncements': getGlobalAnnouncements(user) }
	return render_to_response('main/settings.html', content,
		context_instance=RequestContext(request))
	
def updateSetting(request):
	user = request.user

	year = datetime.date.today().year
	semester = currentSemester()
	class_list = class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester).order_by('department', 'class_number')

	message = ''
	if request.method == 'POST':
		form = SettingForm(request.POST)
		if form.is_valid():
			getSetting = Setting.objects.filter(uid=user.id).update(email_announcement=form.cleaned_data['email_announcement'], email_activity=form.cleaned_data['email_activity'])
			message = 'You have successfully updated your settings.'
	else:
		setting = Setting.objects.get(uid=user.id)
		form = SettingForm(initial={'email_announcement': setting.email_announcement, 'email_activity': setting.email_activity})

	content = {'class_list': class_list, 'form': form, 'message': message, 'globalAnnouncements': getGlobalAnnouncements(user) }
	return render_to_response('main/settings.html', content,
		context_instance=RequestContext(request))	

def currentSemester():
	# this is just to return the time and date for the bottom right of the top banner
	today = datetime.date.today()
	currentYear = today.year
	nextYear = currentYear+1
	startSpring = date(nextYear, 1, 1)
	startSummer = date(currentYear, 5, 1)
	startFall = date(currentYear, 9, 1)
	if today < startSummer:
		return 'Spring'
	elif today < startFall:
		return 'Summer'
	elif today < startSpring:
		return 'Fall'
	else: 
		return 0
		
def getGlobalAnnouncements(user):
	cids = []
	classes = ClassList.objects.filter(uid=user.id)
	for c in classes:
		cids.append(c.cid)
	latestAnnouncements = Announcement.objects.filter(cid__in=cids).order_by('-date_posted')[:4]
	for announcement in latestAnnouncements:
		if (datetime.datetime.now() - announcement.date_posted) < timedelta(days=1):
			announcement.isNew = 1
		else:
			announcement.isNew = 0
		if len(announcement.title) > 15:
			announcement.title = announcement.title[:15] + '...' 

		if len(announcement.content) > 100:
			announcement.content = announcement.content[:100] + '...'
	return latestAnnouncements
