from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from Main.models import Course, Setting, ClassList, UserProfile
from datetime import date
from Instructor.forms import SettingForm
from Instructor.models import Announcement
from Calendar.models import Event
from django.contrib.auth import authenticate, login
import datetime, os, calendar
from itertools import chain
from operator import attrgetter
from datetime import timedelta

#This is just for the index page when user first reaches website


# Create your views here.
def index(request):
	user = request.user
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester).order_by('department', 'class_number')
	old_class_list = Course.objects.filter(classlist__uid=user.id, year__lt=year).order_by('-year', 'department', 'class_number')
	
	# Get calendar info for the user for the side cal
	if request.user.is_authenticated():
		side_cal = getCalendarContent(user, class_list)
	else:
		side_cal = { 'no_cal': 'no cal' }
	main_content={'class_list': class_list, 'old_class_list': old_class_list, 'globalAnnouncements': getGlobalAnnouncements(user)}
	
	content = dict(side_cal.items() + main_content.items())
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
			return HttpResponseRedirect("/accounts/settings/update/")
	else:
		try:
			setting = Setting.objects.get(uid=user.id)
			return HttpResponseRedirect("/accounts/settings/update/")
		except Setting.DoesNotExist:
			form = SettingForm()
		
	# Get calendar info for the user for the side cal
	side_cal = getCalendarContent(user, class_list)
	main_content = {'class_list': class_list, 'form': form, 'message': message, 'globalAnnouncements': getGlobalAnnouncements(user) }
	
	content = dict(side_cal.items() + main_content.items())
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
	
	# Get calendar info for the user for the side cal
	side_cal = getCalendarContent(user, class_list)
	main_content = {'class_list': class_list, 'form': form, 'message': message, 'globalAnnouncements': getGlobalAnnouncements(user) }

	content = dict(side_cal.items() + main_content.items())
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
	latestAnnouncements = Announcement.objects.filter(cid__in=cids).order_by('-date_posted')[:3]
	for announcement in latestAnnouncements:
		if (datetime.datetime.now() - announcement.date_posted) < timedelta(days=1):
			announcement.isNew = 1
		else:
			announcement.isNew = 0
		if len(announcement.title) > 13:
			announcement.title = announcement.title[:13] + '...' 

		if len(announcement.content) > 100:
			announcement.content = announcement.content[:100] + '...'
	return latestAnnouncements

# Method to retrieve calendar info for sidebar
def getCalendarContent(user, class_list):
	cal = calendar.Calendar(6)
	curr_date = datetime.datetime.today()

	month_name = { '1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December' }		

	year = curr_date.year
	month = {'name': curr_date.strftime("%B"), 'number': curr_date.month }

	all_weeks = getCalendar(cal, curr_date.year, curr_date.month)
	days_with_events = getEvents(user, class_list, year, month['number'])
	content = { 'days_with_events': days_with_events, 'all_weeks': all_weeks, 'year': year, 'month': month }
	return content

# Method for retrieving the current calendar for getCalendarContent method
def getCalendar(cal, year, month):
	cal_month = cal.itermonthdays(year, month)
	all_weeks = []
	week = []
	count = 0
	for day in cal_month:
		week.append(day)
		count = count + 1
		if count == 7:
			all_weeks.append(week)
			week = []
			count = 0
	return all_weeks

# Method to get the events for a month for getCalendarContent method
def getEvents(user, class_list, year, month):
	# Get all events created by the user
	custom_events = Event.objects.filter(uid=user, date__year=year, date__month=month).order_by('date')

	# Get all events for the classes for which the student is enrolled in
	events_chain = chain(custom_events)
	for course in class_list:
		if user.userprofile in UserProfile.objects.filter(classlist__cid=course.cid, classlist__is_ta=0, classlist__is_instructor=0):
			events_chain = chain(Event.objects.filter(cid=course.cid, date__year=year, date__month=month), events_chain)

	# Chain all events retrieved into one events queryset
	events = sorted(events_chain, key=attrgetter('date'))

	day_of_month = range(1, calendar.monthrange(year, month)[1]+1)
	days_with_events = {}

	def getEventsForDay(event):
		if event.date.day == day:
			return event

	for day in day_of_month:
		all_days_events = filter(getEventsForDay, events)
		if all_days_events:
			if all_days_events.count <= 4:
				limit_events = all_days_events
			elif all_days_events.count > 4:
				limit_events = all_days_events[:4]
			for event in limit_events:
				# Don't count the first 5 spaces as characters in the length of the event name
				tempLength = event.event_name.replace(' ', '', 5)
				if len(tempLength) > 8:
					event.event_name = event.event_name[:8] + '...'
			days_with_events[day] = { 'limit': limit_events, 'all': all_days_events, 'total': len(all_days_events) }

	return days_with_events

# Methods for handling file uploads

# Check that file is a desired type (extension)
def checkFileType(uploaded_file, desired_file_types):
	file_ext = os.path.splitext(uploaded_file.name)[1]
	if file_ext in desired_file_types:
		return True
	else:
		return False

# Check that file is less than or equal to the desired max file size (in Bytes)
def checkFileSize(uploaded_file, max_file_size):
	file_size = uploaded_file.size
	if file_size <= max_file_size:
		return True
	else:
		return False