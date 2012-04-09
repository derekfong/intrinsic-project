# Calendar Views
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from itertools import chain
from operator import attrgetter
import calendar, datetime, random

from Student.views import getClassList, getStudents
from Calendar.models import Event, Label
from Calendar.forms import EventForm, LabelForm, CalendarForm

#View to generate the page for the main view of Calendar App
def index(request):
	all_classes = getClassList(request.user)
	
	cal = calendar.Calendar(6)
	curr_date = datetime.datetime.today()
	
	day = curr_date.day
	month_name = { '1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December' }		
	
	if request.method == 'POST':
		form = CalendarForm(request.POST)
		if form.is_valid():
			year = int(request.POST['year'])
			month = { 'name': month_name[request.POST['month']], 'number': int(request.POST['month']) }
			all_weeks = getCalendar(cal, year, month['number'])
			days_with_events = getEvents(request.user, all_classes, year, month['number'])
	else:
		form = CalendarForm()
		all_weeks = getCalendar(cal, curr_date.year, curr_date.month)
		year = curr_date.year
		month = {'name': curr_date.strftime("%B"), 'number': curr_date.month }
		days_with_events = getEvents(request.user, all_classes, year, month['number'])
		
	context = { 'form': form, 'days_with_events': days_with_events, 'all_weeks': all_weeks, 
				'year': year, 'month': month, 'day': day, 'curr_date': curr_date }
	return render_to_response('calendar/index.html', context, RequestContext(request))

# View for displaying all events for a particular day
def day_events(request, year, month, day):
	all_classes = getClassList(request.user)
	
	month_name = { '1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December' }		
	
	month_name = month_name[month]
	selected_day = { 'year': year, 'month': month_name, 'day': day }

	# Get all events created by the user for the specified day
	custom_events = Event.objects.filter(uid=request.user, date__year=year, date__month=month, date__day=day).order_by('date')
	
	# Get all events for that day for the classes for which the student is enrolled in
	events_chain = chain(custom_events)
	for course in all_classes:
		if request.user.userprofile in getStudents(course.cid):
			events_chain = chain(Event.objects.filter(cid=course.cid, date__year=year, date__month=month, date__day=day), events_chain)
	
	# Chain all events retrieved into one events queryset
	events = sorted(events_chain, key=attrgetter('date'))
	
	context = { 'events': events, 'selected_day': selected_day }
	return render_to_response('calendar/day_events.html', context, RequestContext(request))

# View for creating a new event
def event(request):
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			event_name = request.POST['event_name']
			date = request.POST['date']
			location = request.POST['location']
			label = Label.objects.get(lid=request.POST['lid'])
			description = request.POST['description']
			event = Event(uid=request.user.userprofile, event_name=event_name, date=date, location=location, lid=label, description=description)
			event.save()
			return HttpResponseRedirect("/calendar")
	else:
		form = EventForm()

	context = { 'form': form }
	return render_to_response('calendar/event.html', context, RequestContext(request))

# View for creating a label
def label(request):
	if request.method == 'POST':
		form = LabelForm(request.POST)
		if form.is_valid():
			label_name = request.POST['name']
			color = request.POST['color']
			label = Label(name=label_name, color=color)
			label.save()
			return HttpResponseRedirect("/calendar/event")
	else:
		form = LabelForm()

	context = { 'form': form, }
	return render_to_response('calendar/label.html', context, RequestContext(request))

# Method to retrieve a calendar
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

# Method to get the events for a month
def getEvents(user, all_classes, year, month):
	# Get all events created by the user
	custom_events = Event.objects.filter(uid=user, date__year=year, date__month=month).order_by('date')
	
	# Get all events for the classes for which the student is enrolled in
	events_chain = chain(custom_events)
	for course in all_classes:
		if user.userprofile in getStudents(course.cid):
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

# Method for getting or creating a label for a particular class
def getClassLabel(cid, department, class_number):
	name = department +" "+ class_number
	COLOR_CHOICES = ['Cyan', 'Blue', 'Lime', 'Fuchsia', 'Silver', 'Brown', 'Maroon', 
		'Olive', 'Plum', 'Thistle', 'Turquoise', 'Gold', 'Chocolate', 'Pink']
	color = random.choice(COLOR_CHOICES)
	try:
		label = Label.objects.get(cid=cid)
	except Label.DoesNotExist:	
		label = Label(cid=cid, name=name, color=color)
		label.save()
	return label