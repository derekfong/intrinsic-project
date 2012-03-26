from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from Main.models import Course
from datetime import date
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
	
#def class_view(request):
	#class = get_object_or_404(Course, )

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