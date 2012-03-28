from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from Main.models import Course, Setting
from datetime import date
from forms import SettingForm
import datetime

# Create your views here.
def index(request):
	user = request.user
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	old_class_list = Course.objects.filter(classlist__uid=user.id, year__lt=year)
	return render_to_response('main/index.html', {'class_list': class_list, 'old_class_list': old_class_list},
		context_instance=RequestContext(request))

def logout_view(request):
	auth.logout(request)
	return HttpResponseRedirect("/")
	
def setting(request):
	user = request.user
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
	if request.method == 'POST':
		setting = Setting(uid=user.userprofile)
		form = SettingForm(request.POST, instance=setting)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		try:
			setting = Setting.objects.get(uid=user.id)
			return HttpResponseRedirect("/accounts/settings/update/")
		except Setting.DoesNotExist:
			form = SettingForm()
		
	return render_to_response('main/settings.html', {'class_list': class_list, 'form': form },
		context_instance=RequestContext(request))
	
def updateSetting(request):
	user = request.user

	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)

	if request.method == 'POST':
		form = SettingForm(request.POST)
		if form.is_valid():
			getSetting = Setting.objects.filter(uid=user.id).update(email_announcement=form.cleaned_data['email_announcement'], email_activity=form.cleaned_data['email_activity'])
			return HttpResponseRedirect("/accounts/settings/update")
	else:
		setting = Setting.objects.get(uid=user.id)
		form = SettingForm(initial={'email_announcement': setting.email_announcement, 'email_activity': setting.email_activity})

	return render_to_response('main/settings.html', {'class_list': class_list, 'form': form },
		context_instance=RequestContext(request))	

def currentSemester():
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