# Calendar Views
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from itertools import chain
from operator import attrgetter
import calendar, datetime, random

from Main.views import getGlobalAnnouncements
from Student.views import getClassList, getStudents
from Calendar.models import Event, Label
from Calendar.forms import EventForm, LabelForm, CalendarForm

#View to generate the page for the main view of Calendar App
def index(request):
	class_list = getClassList(request.user)
	
	cal = calendar.Calendar(6)
	curr_date = datetime.datetime.today()
	
	month_name = { '1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December' }		
	
	if request.method == 'POST':
		form = CalendarForm(request.POST)
		if form.is_valid():
			curr_month = int(request.POST.__getitem__('curr_month'))
			curr_year = int(request.POST.__getitem__('curr_year'))
			# If previous month is selected, get the previous month and associated year
			if 'prev_month' in request.POST:
				prev_month = curr_month - 1
				if prev_month == 0:
					prev_month = 12
					year = curr_year - 1
				else:
					year = curr_year
				month = { 'name': month_name[str(prev_month)], 'number': prev_month }
				all_weeks = getCalendar(cal, year, month['number'])
			# Else if next month is selected, get the next month and associated year
			elif 'next_month' in request.POST:
				next_month = curr_month + 1
				if next_month == 13:
					next_month = 1
					year = curr_year + 1
				else:
					year = curr_year
				month = { 'name': month_name[str(next_month)], 'number': next_month }
				all_weeks = getCalendar(cal, year, month['number'])
			# Otherwise, return the current month and associated year
			else:
				year = int(form.cleaned_data['year'])
				month = { 'name': month_name[form.cleaned_data['month']], 'number': int(form.cleaned_data['month']) }
			all_weeks = getCalendar(cal, year, month['number'])
			days_with_events = getEvents(request.user, class_list, year, month['number'])
	else:
		form = CalendarForm()
		all_weeks = getCalendar(cal, curr_date.year, curr_date.month)
		year = curr_date.year
		month = {'name': curr_date.strftime("%B"), 'number': curr_date.month }
		days_with_events = getEvents(request.user, class_list, year, month['number'])
		
	context = { 'form': form, 'days_with_events': days_with_events, 'all_weeks': all_weeks, 'year': year, 'month': month, 
		'globalAnnouncements': getGlobalAnnouncements(request.user), 'class_list': class_list }
	return render_to_response('calendar/index.html', context, RequestContext(request))

# View for displaying all events for a particular day
def day_events(request, year, month, day):
	class_list = getClassList(request.user)
	
	month_name = { '1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December' }		
	
	month_name = month_name[month]
	selected_day = { 'year': year, 'month': month_name, 'day': day }

	# Get all events created by the user for the specified day
	custom_events = Event.objects.filter(uid=request.user, date__year=year, date__month=month, date__day=day).order_by('date')
	
	# Get all events for that day for the classes for which the student is enrolled in
	events_chain = chain(custom_events)
	for course in class_list:
		if request.user.userprofile in getStudents(course.cid):
			events_chain = chain(Event.objects.filter(cid=course.cid, date__year=year, date__month=month, date__day=day), events_chain)
	
	# Chain all events retrieved into one events queryset
	events = sorted(events_chain, key=attrgetter('date'))
	
	context = { 'events': events, 'selected_day': selected_day, 'globalAnnouncements': getGlobalAnnouncements(request.user),
		'class_list': class_list }
	return render_to_response('calendar/day_events.html', context, RequestContext(request))

# View for creating a new event
def event(request):
	class_list = getClassList(request.user)
	label_error = ''
	if request.method == 'POST':
		form = EventForm(request.POST, uid=request.user.id)
		if 'update_label' in request.POST:
			if form.cleaned_data['lid']:
				label = Label.objects.get(lid=form.cleaned_data['lid'])
				# Check to see if the label is associated to a class
				if label.cid:
					form = EventForm(uid=request.user.id)
					label_error = 'You cannot edit that course label'
				else:
					return HttpResponseRedirect("/calendar/event/label/" + form.cleaned_data['lid'])
			else:
				form = EventForm(uid=request.user.id)
				label_error = 'Please choose a label to edit'
		elif 'create_label' in request.POST:
			return HttpResponseRedirect("/calendar/event/label/")
		elif form.is_valid():
			event_name = form.cleaned_data['event_name']
			date = form.cleaned_data['date']
			location = form.cleaned_data['location']
			label = Label.objects.get(lid=form.cleaned_data['lid'])
			description = form.cleaned_data['description']
			event = Event(uid=request.user.userprofile, event_name=event_name, date=date, location=location, lid=label, description=description)
			event.save()
			return HttpResponseRedirect("/calendar")
	else:
		form = EventForm(uid=request.user.id)
	
	update = 0
	context = { 'form': form, 'label_error': label_error, 'update': update, 'globalAnnouncements': getGlobalAnnouncements(request.user),
	 	'class_list': class_list }
	return render_to_response('calendar/event.html', context, RequestContext(request))

# View for updating an existing event
def update_event(request, year, month, day, eid):
	class_list = getClassList(request.user)
	if request.method == 'POST':
		lid = Label.objects.get(lid=request.POST['lid'])
		event = Event(uid=request.user.userprofile, eid=eid, lid=lid)
		form = EventForm(request.POST, uid=request.user.userprofile, instance=event)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("..")
	else:
		tmp = Event.objects.get(eid=eid)
		existing_event = { 'lid': tmp.lid, 'event_name': tmp.event_name, 'date': tmp.date, 'location': tmp.location, 'description': tmp.description }
		form = EventForm(uid=request.user.id, initial=existing_event)
		
	update = 1
	context = { 'form': form, 'update': update, 'globalAnnouncements': getGlobalAnnouncements(request.user),
	 	'class_list': class_list }
	return render_to_response('calendar/event.html', context, RequestContext(request))

# View for removing an existing event
def remove_event(request, year, month, day, eid):
	event = Event.objects.get(eid=eid)
	event.delete()
	return HttpResponseRedirect("/calendar/%s" %year + '/%s' %month + '/%s' %day)

# View for creating a label
def label(request):
	class_list = getClassList(request.user)
	if request.method == 'POST':
		form = LabelForm(request.POST)
		if 'update_label' in request.POST:
			return HttpResponseRedirect("/calendar/event/" + form.cleaned_data['lid'])
		elif form.is_valid():
			user = request.user
			label_name = form.cleaned_data['name']
			color = form.cleaned_data['color']
			label = Label(uid=user.userprofile, name=label_name, color=color)
			label.save()
			return HttpResponseRedirect("/calendar/event")
	else:
		form = LabelForm()
		
	update = 0
	context = { 'form': form, 'update': update, 'globalAnnouncements': getGlobalAnnouncements(request.user),
	 	'class_list': class_list }
	return render_to_response('calendar/label.html', context, RequestContext(request))

# View for updating a label
def update_label(request, lid):
	class_list = getClassList(request.user)
	if request.method == 'POST':
		label = Label(uid=request.user.userprofile, lid=lid)
		form = LabelForm(request.POST, instance=label)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/calendar/event")
	else:
		tmp = Label.objects.get(lid=lid)
		form = LabelForm(initial={ 'name': tmp.name, 'color': tmp.color })
		
	update = 1
	context = { 'form': form, 'update': update, 'globalAnnouncements': getGlobalAnnouncements(request.user),
	 	'class_list': class_list }
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
def getEvents(user, class_list, year, month):
	# Get all events created by the user
	custom_events = Event.objects.filter(uid=user, date__year=year, date__month=month).order_by('date')
	
	# Get all events for the classes for which the student is enrolled in
	events_chain = chain(custom_events)
	for course in class_list:
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
def getClassLabel(user, cid, department, class_number):
	name = department +" "+ class_number
	COLOR_CHOICES = ['Cyan', 'Blue', 'Lime', 'Fuchsia', 'Silver', 'Brown', 'Maroon', 
		'Olive', 'Plum', 'Thistle', 'Turquoise', 'Gold', 'Chocolate', 'Pink']
	color = random.choice(COLOR_CHOICES)
	try:
		label = Label.objects.get(cid=cid)
	except Label.DoesNotExist:	
		label = Label(uid=user.userprofile, cid=cid, name=name, color=color)
		label.save()
	return label