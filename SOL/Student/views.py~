from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from Main.models import Course, ClassList, UserProfile
from django.contrib.auth.models import User
from Instructor.models import Activity, Announcement, CourseContent, Slide
from Main.views import currentSemester
#from reportlab.pdfgen import canvas
from django.http import HttpResponse
import datetime

# Create your views here.
def index(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user
	
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	students = getStudents(class_id)
	enrolled = getEnrolled(class_id)
	
	latestAnnouncements = getAnnouncements(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	accessToStudent = studentAccess(enrolled, user)
	isCurrent = checkCurrent(c)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
	content = {'class': c , 'instructors': instructors, 'tas': tas, 'students': students, 'accessToInst': accessToInst, 
		'accessToStudent': accessToStudent, 'latestAnnouncements': latestAnnouncements, 'classUrl': getClassUrl(c), 'class_list': class_list, 
		'isCurrent': isCurrent }
	
	return render_to_response('student/index.html', content,
		context_instance=RequestContext(request))
		
def syllabus(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	enrolled = getEnrolled(class_id)
	
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	students = getStudents(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	accessToStudent = studentAccess(enrolled, user)
	isCurrent = checkCurrent(c)
	
	latestAnnouncements = getAnnouncements(class_id)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
	message = ''
	try:
		syllabus = CourseContent.objects.get(cid = class_id)
	except CourseContent.DoesNotExist:
		message = 'No syllabus has been created for this class.'
		###########TRY TO FIND A BETTER WAY TO SEND A BLANK SYLLABUS
		syllabus = []
		##########
		
	content = {'class': c, 'accessToStudent': accessToStudent, 'accessToInst': accessToInst, 'syllabus': syllabus, 
	'latestAnnouncements': latestAnnouncements, 'classUrl': getClassUrl(c), 'students': students, 'tas': tas, 'instructors': instructors,
	'message': message, 'class_list': class_list, 'isCurrent': isCurrent}
	return render_to_response('student/syllabus.html', content, 
		context_instance=RequestContext(request))

def slides(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)

	user = request.user
	enrolled = getEnrolled(class_id)

	instructors = getInsts(class_id)
	tas = getTas(class_id)
	students = getStudents(class_id)

	accessToInst = instAccess(instructors, tas, user)
	accessToStudent = studentAccess(enrolled, user)
	isCurrent = checkCurrent(c)

	latestAnnouncements = getAnnouncements(class_id)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
		
	slides = Slide.objects.filter(cid = class_id)

	content = {'class': c, 'accessToStudent': accessToStudent, 'accessToInst': accessToInst, 'latestAnnouncements': latestAnnouncements, 
	'classUrl': getClassUrl(c),  'class_list': class_list, 'slides': slides, 'isCurrent': isCurrent}
	return render_to_response('student/slides.html', content, 
		context_instance=RequestContext(request))
	
def activities(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user

	instructors = getInsts(class_id)
	tas = getTas(class_id)
	students = getStudents(class_id)
	enrolled = getEnrolled(class_id)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
	activities = Activity.objects.filter(cid=class_id).order_by('due_date')
	for activity in activities:
		activity.pastDue = pastDue(activity)
		
	latestAnnouncements = getAnnouncements(class_id)

	accessToStudent = studentAccess(enrolled, user)
	accessToInst = instAccess(instructors, tas, user)
	isCurrent = checkCurrent(c)
	
	content = {'accessToStudent': accessToStudent, 'accessToInst': accessToInst, 'class': c, 'activities': activities, 
	'latestAnnouncements': latestAnnouncements, 'classUrl': getClassUrl(c), 'class_list': class_list, 'isCurrent': isCurrent}
	return render_to_response('student/activities.html', content, 
		context_instance=RequestContext(request))

def announcements(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user

	instructors = getInsts(class_id)
	tas = getTas(class_id)
	students = getStudents(class_id)
	enrolled = getEnrolled(class_id)

	announcements = Announcement.objects.filter(cid=class_id).order_by('-date_posted')
	latestAnnouncements = getAnnouncements(class_id)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)

	accessToStudent = studentAccess(enrolled, user)
	accessToInst = instAccess(instructors, tas, user)
	isCurrent = checkCurrent(c)
	
	content = {'accessToStudent': accessToStudent, 'accessToInst': accessToInst, 'class': c, 'announcements': announcements, 
	'latestAnnouncements': latestAnnouncements, 'classUrl': getClassUrl(c), 'class_list': class_list, 'isCurrent': isCurrent }
	
	return render_to_response('student/announcements.html', content, 
		context_instance=RequestContext(request))			
		
def getAnnouncements(class_id):
	latestAnnouncements = Announcement.objects.filter(cid=class_id).order_by('-date_posted')[:3]
	for announcement in latestAnnouncements:
		if len(announcement.title) > 25:
			announcement.title = announcement.title[:25] + '...' 
		else:
			announcement.title = announcement.title
			
		if len(announcement.content) > 100:
			announcement.content = announcement.content[:100] + '...'
		else:
			announcement.content = announcement.content
	return latestAnnouncements	
	
def pastDue(activity):
	if datetime.datetime.now() > activity.due_date:
		return 1
	else:
		return 0

def instAccess(instructors, tas, user):
	for ta in tas:
		if user.id == ta.user.id:
			return 1
	for instructor in instructors:
		if user.id == instructor.user.id:
			return 1
	return 0

def studentAccess(students, user):
	for student in students:
		if user.id == student.user.id:
			return 1
	return 0

def getInsts(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id, classlist__is_instructor=1)

def getTas(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id, classlist__is_ta=1)

def getStudents(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id, classlist__is_ta=0, classlist__is_instructor=0)
	
def getEnrolled(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id)
		
def getClassUrl(c):
	classUrl = '/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/'
	return classUrl
	
def checkCurrent(c):
	year = datetime.date.today().year
	semester = currentSemester()
	
	if year == c.year and semester == c.semester:
		return 1
	else:
		return 0
	
	
	
	
	