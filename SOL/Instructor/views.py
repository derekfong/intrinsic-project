from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from Main.models import Course, ClassList
from Instructor.models import Announcement, Activity
from Student.views import instAccess, getInsts, getTas, getStudents
from forms import AnnounceForm, ActivityForm
import datetime

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
	
	return render_to_response('instructor/syllabus.html', {'class': c, 'accessToInst': accessToInst, }, 
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
			return HttpResponseRedirect("../")
	else:
		form = ActivityForm()
	
	return render_to_response('instructor/activity.html', {'class': c, 'accessToInst': accessToInst, 'form': form, 'activities': activities}, 
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
		announce = Announcement(cid=c, uid=user.userprofile, date_posted=datetime.datetime.now())
		form = AnnounceForm(request.POST, instance=announce)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		form = AnnounceForm()
	
	return render_to_response('instructor/announcement.html', {'c': c, 'form': form, 'accessToInst': accessToInst, 'announcements': announcements }, 
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
		announce = Announcement(cid=c, uid=user.userprofile, date_posted=datetime.datetime.now())
		form = AnnounceForm(request.POST, instance=announce)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		form = AnnounceForm()

	return render_to_response('instructor/grades.html', {'c': c, 'form': form, 'accessToInst': accessToInst, 'announcements': announcements , 'students': students}, 
		context_instance=RequestContext(request))
		
#def getRequiredContent(department, class_number, year, semester, section):
	