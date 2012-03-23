from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from Main.models import Course, ClassList
from Instructor.models import Announcement, Activity, CourseContent
from Gradebook.models import UploadGrade
from Student.views import instAccess, getInsts, getTas, getStudents
from forms import AnnounceForm, ActivityForm, CourseForm
import datetime
from reportlab.pdfgen import canvas

# Create your views here.
def index(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
		
	return render_to_response('instructor/index.html', {'class': c, 'accessToInst': accessToInst, },
		context_instance=RequestContext(request))

def syllabus(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	
	if request.method == 'POST':
		content = CourseContent(cid=class_id)
		form = CourseForm(request.POST, instance=content)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		count = CourseContent.objects.filter(cid=class_id).count()
		if count == 1:
			course = CourseContent.objects.get(cid=class_id)
			form = CourseForm(initial={'officeHrs': course.officeHrs, 'officeLocation': course.officeLocation, 'phoneNumber': course.phoneNumber, 'TaOfficeLocation': course.TaOfficeLocation, 'TaOfficeHrs': course.TaOfficeHrs, 'lectTime': course.lectTime, 'prereq': course.prereq, 'books': course.books, 'topics': course.topics, 'markingScheme': course.markingScheme, 'academicHonesty': course.academicHonesty, 'additionalInfo': course.additionalInfo, 'file_path': course.file_path,})
		else:
			form = CourseForm()
	
	return render_to_response('instructor/syllabus.html', {'class': c, 'accessToInst': accessToInst, 'form': form}, 
		context_instance=RequestContext(request))
			
		
def activity(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	activities = Activity.objects.filter(cid=class_id)
	
	if request.method == 'POST':
		activity = Activity(cid=c)
		form = ActivityForm(request.POST, instance=activity)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		form = ActivityForm()
	
	return render_to_response('instructor/activity.html', {'class': c, 'accessToInst': accessToInst, 'form': form, 'activities': activities, 'update':0}, 
		context_instance=RequestContext(request))
		
def updateActivity(request, department, class_number, year, semester, section, aid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	a = get_object_or_404(Activity, pk=aid)

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)

	accessToInst = instAccess(instructors, tas, user)
	activities = Activity.objects.filter(cid=class_id)

	if request.method == 'POST':
		activity = Activity(cid=c, aid=aid)
		form = ActivityForm(request.POST, instance=activity)
		if form.is_valid():
			form.save()
			url ='/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/instructor/activity'
			return HttpResponseRedirect(url)
	else:
		tmp = Activity.objects.get(aid=aid)
		form = ActivityForm(initial={'activity_name': tmp.activity_name, 'out_of': tmp.out_of, 'worth': tmp.worth, 'due_date': tmp.due_date, 'status': tmp.status, })

	return render_to_response('instructor/activity.html', {'class': c, 'accessToInst': accessToInst, 'form': form, 'activities': activities, 'update':1}, 
		context_instance=RequestContext(request))
		
def removeActivity(request, department, class_number, year, semester, section, aid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	a = get_object_or_404(Activity, pk=aid)

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)

	accessToInst = instAccess(instructors, tas, user)

	if accessToInst:
		activity = Activity.objects.get(aid=aid)
		activity.delete()
		url ='/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/instructor/activity'
		return HttpResponseRedirect(url)
	else:
		return render_to_response('instructor/announcement.html', {'accessToInst': accessToInst, }, 
			context_instance=RequestContext(request))
		
def announcement(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	announcements = Announcement.objects.filter(cid=class_id).order_by('-date_posted')
	
	if request.method == 'POST':
		announce = Announcement(cid=c, uid=user.userprofile, was_updated=0, updated_on=datetime.datetime.now(), updated_by=user.userprofile, date_posted=datetime.datetime.now())
		form = AnnounceForm(request.POST, instance=announce)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		form = AnnounceForm()
	
	return render_to_response('instructor/announcement.html', {'c': c, 'form': form, 'accessToInst': accessToInst, 'announcements': announcements }, 
		context_instance=RequestContext(request))
		
def updateAnnouncement(request, department, class_number, year, semester, section, anid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	an = get_object_or_404(Announcement, pk=anid)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	announcements = Announcement.objects.filter(cid=class_id).order_by('-date_posted')
	
	if request.method == "POST":
		announce = Announcement(cid=c, date_posted=an.date_posted, uid=an.uid, was_updated=1, updated_by=user.userprofile, updated_on=datetime.datetime.now(), anid=anid)
		form = AnnounceForm(request.POST, instance=announce)
		if form.is_valid():
			form.save()
			url ='/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/instructor/announcement'
			return HttpResponseRedirect(url)
	else:
		tmp = Announcement.objects.get(anid=anid)
		form = AnnounceForm(initial={'title': tmp.title, 'content': tmp.content })
	return render_to_response('instructor/announcement.html', {'form': form, 'announcements': announcements, 'accessToInst': accessToInst }, 
		context_instance=RequestContext(request))

def removeAnnouncement(request, department, class_number, year, semester, section, anid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	an = get_object_or_404(Announcement, pk=anid)

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)

	accessToInst = instAccess(instructors, tas, user)

	if accessToInst:
		announcement = Announcement.objects.get(anid=anid)
		announcement.delete()
		url ='/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/instructor/announcement'
		return HttpResponseRedirect(url)
	else:
		return render_to_response('instructor/announcement.html', {'accessToInst': accessToInst, }, 
			context_instance=RequestContext(request))

def grades(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)

	accessToInst = instAccess(instructors, tas, user)
	students = getStudents(class_id)
	
	if request.method == 'POST':
		#announce = Announcement(cid=c, uid=user.userprofile, date_posted=datetime.datetime.now())
		form = UploadGrade(request.POST, request.FILES)
		#if form.is_valid():
		#	form.save()
		#	return HttpResponseRedirect("")
	else:
		form = UploadGrade()

	return render_to_response('instructor/grades.html', {'c': c, 'form': form, 'accessToInst': accessToInst, 'students': students}, 
		context_instance=RequestContext(request))
		
#def getRequiredContent(department, class_number, year, semester, section):
	
