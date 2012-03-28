from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
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
	# gets corresponding classes to display on the website
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	content = getContent(c, user)
	
	return render_to_response('student/index.html', content,
		context_instance=RequestContext(request))
		
def syllabus(request, department, class_number, year, semester, section):
	# grab corresponding syllabus for that class
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
		
	message = ''
	try:
		syllabus = CourseContent.objects.get(cid = c.cid)
	except CourseContent.DoesNotExist:
		message = 'No syllabus has been created for this class.'
		syllabus = []
		
	content = getContent(c, user)
	content['syllabus'] = syllabus
	content['message'] = message
	
	return render_to_response('student/syllabus.html', content, 
		context_instance=RequestContext(request))

def slides(request, department, class_number, year, semester, section):
	# slides are lecture notes 
	# student has to find corresponding sildes for that course...
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
		
	slides = Slide.objects.filter(cid = c.cid)

	content = getContent(c, user)
	content['slides'] = slides

	return render_to_response('student/slides.html', content, 
		context_instance=RequestContext(request))
	
def activities(request, department, class_number, year, semester, section):
	# activities are assignments, exams, midterms, etc	
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	activities = Activity.objects.filter(cid=c.cid).order_by('due_date')
	for activity in activities:
		activity.pastDue = pastDue(activity)
	
	content = getContent(c, user)
	content['activities'] = activities
	
	return render_to_response('student/activities.html', content, 
		context_instance=RequestContext(request))

def announcements(request, department, class_number, year, semester, section):
	# instructors can leave annoucement messages on the home page for students to view 
	# they log in
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)

	announcements = Announcement.objects.filter(cid=c.cid).order_by('-date_posted')

	content = getContent(c, user)
	content['announcements'] = announcements
	
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

# sees if there is permission as instructor/marker
# Diff features depending on permission.
def instAccess(instructors, tas, user):
	for ta in tas:
		if user.id == ta.user.id:
			return 1
	for instructor in instructors:
		if user.id == instructor.user.id:
			return 1
	return 0

# sees if there is permission as student.
# Diff features depending on permission.
def studentAccess(students, user):
	for student in students:
		if user.id == student.user.id:
			return 1
	return 0


# SETTERS AND GETTERS from models
def getInsts(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id, classlist__is_instructor=1)

def getTas(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id, classlist__is_ta=1)

def getStudents(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id, classlist__is_ta=0, classlist__is_instructor=0).order_by('user__last_name', 'user__first_name', 'sfu_id')
	
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
	
def getClassList(user):
	year = datetime.date.today().year
	semester = currentSemester()
	return Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
def getClassObject(department, class_number, year, semester, section, user):
	try:
		class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	except Course.DoesNotExist:
		raise Http404

	return get_object_or_404(Course, pk=class_id)


# actually display content on the main page relating to the student user
def getContent(c, user):
	instructors = getInsts(c.cid)
	tas = getTas(c.cid)
	students = getStudents(c.cid)
	enrolled = getEnrolled(c.cid)

	content = {'class': c , 'instructors': instructors, 
		'tas': tas, 'students': students, 'accessToInst': instAccess(instructors, tas, user), 
		'accessToStudent': studentAccess(enrolled, user), 'latestAnnouncements': getAnnouncements(c.cid), 'classUrl': getClassUrl(c), 
		'class_list': getClassList(user), 'isCurrent': checkCurrent(c) }
	return content
