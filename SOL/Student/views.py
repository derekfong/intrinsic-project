from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from Main.models import Course, ClassList, UserProfile
from django.contrib.auth.models import User
from Instructor.models import Activity, Announcement, CourseContent
from reportlab.pdfgen import canvas
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
	
	content = {'class': c , 'instructors': instructors, 'tas': tas, 'students': students, 'accessToInst': accessToInst, 
		'accessToStudent': accessToStudent, 'latestAnnouncements': latestAnnouncements}
	
	return render_to_response('student/index.html', content,
		context_instance=RequestContext(request))
		
def syllabus(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user
	enrolled = getEnrolled(class_id)
	accessToStudent = studentAccess(enrolled, user)
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	# Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(mimetype='application/pdf')
	response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

    # Create the PDF object, using the response object as its "file."
	p = canvas.Canvas(response)
	p.setLineWidth(.3)
	p.setFont('Helvetica', 12)
	
	content = CourseContent.objects.get(cid=class_id)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
	yaxis=750
	p.drawCentredString(200, yaxis, '%s' %c.class_name)
	yaxis -= 20
	p.drawCentredString(250, yaxis, '%s ' %c.semester + '%s' %c.year)
	yaxis -= 20
	
	if instructors.count() > 0:
		p.drawString(50, yaxis, 'Instructors')
		yaxis -= 10
		p.line(50,yaxis,580, (yaxis-10))
		yaxis -= 10
		for instructor in instructors:
			p.drawString(70, yaxis, 'Name: ' + '%s ' %instructor.user.first_name + '%s' %instructor.user.last_name)
			yaxis -= 20
			p.drawString(70, yaxis, 'Email: ' + '%s' %instructor.user.email)
			yaxis -= 20
			p.drawString(70, yaxis, 'Office Hours: ' + '%s ' %content.officeHrs)
			yaxis -= 20
			p.drawString(70, yaxis, 'Office Location: ' + '%s ' %content.officeLocation)
			yaxis -= 20
			
	if tas.count() > 0:
		p.drawString(50, yaxis, 'Teaching Assitants')
		yaxis -= 10
		p.line(480,yaxis,580,yaxis)
		yaxis -= 10
		for ta in tas:
			p.drawString(70, yaxis, 'Name: ' + '%s ' %ta.user.first_name + '%s' %ta.user.last_name)
			yaxis -= 20
			p.drawString(70, yaxis, 'Email: ' + '%s' %ta.user.email)
			yaxis -= 20
			p.drawString(70, yaxis, 'Office Hours: ' + '%s ' %content.TaOfficeHrs)
			yaxis -= 20
			p.drawString(70, yaxis, 'Office Location: ' + '%s ' %content.TaOfficeLocation)
			yaxis -= 20
			
	p.drawString(50, yaxis, 'Other Information')
	yaxis -= 20
	p.drawString(70, yaxis, 'Lecture Time: ' + '%s ' %content.lectTime)
	yaxis -= 20
	p.drawString(70, yaxis, 'Pre-Requisites: ' + '%s ' %content.prereq)
	yaxis -= 20
	p.drawString(70, yaxis, 'Marking Scheme: ' + '%s ' %content.markingScheme)
	yaxis -= 20
	p.drawString(70, yaxis, 'Academic Honesty: ' + '%s ' %content.academicHonesty)
	yaxis -= 20
	p.drawString(70, yaxis, 'Additional Information: ' + '%s ' %content.additionalInfo)	
	yaxis -= 20
	#p.drawText('Additional Information: ' + '%s ' %content.additionalInfo)

    # Close the PDF object cleanly, and we're done.
	p.showPage()
	p.save()
	return response

def activities(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user

	students = getEnrolled(class_id)
	
	activities = Activity.objects.filter(cid=class_id).order_by('due_date')
	for activity in activities:
		activity.pastDue = pastDue(activity)
		
	latestAnnouncements = getAnnouncements(class_id)

	accessToStudent = studentAccess(students, user)
	content = {'accessToStudent': accessToStudent, 'class': c, 'activities': activities, 'latestAnnouncements': latestAnnouncements,}
	return render_to_response('student/activities.html', content, 
		context_instance=RequestContext(request))

def announcements(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user

	students = getEnrolled(class_id)

	announcements = Announcement.objects.filter(cid=class_id).order_by('-date_posted')
	latestAnnouncements = getAnnouncements(class_id)

	accessToStudent = studentAccess(students, user)
	content = {'accessToStudent': accessToStudent, 'class': c, 'announcements': announcements, 'latestAnnouncements': latestAnnouncements }
	
	return render_to_response('student/announcements.html', content, 
		context_instance=RequestContext(request))			
		
def getAnnouncements(class_id):
	latestAnnouncements = Announcement.objects.filter(cid=class_id).order_by('-date_posted')[:3]
	for announcement in latestAnnouncements:
		if len(announcement.title) > 25:
			announcement.title = announcement.title[:25] + '...' 
		else:
			announcement.title = announcement.title
			
		if len(announcement.content) > 50:
			announcement.content = announcement.content[:50] + '...'
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