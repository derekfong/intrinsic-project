from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from Main.models import Course
from Gradebook.models import Grade, GradeComment
from Instructor.models import Activity
from Student.views import instAccess, studentAccess, getInsts, getTas, getEnrolled
from django.db.models import Avg, Max, Min, Count, StdDev
#from chartit import DataPool, Chart

# Create your views here.

def index(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user
	
	accessToInst = instAccess(getInsts(class_id), getTas(class_id), user)
	accessToStudent = studentAccess(getEnrolled(class_id), user) 
	
	tmpGrades = Grade.objects.filter(aid__cid=class_id, uid=user.id)
	grades = percentAll(tmpGrades)

	return render_to_response('gradebook/index.html', {'class': c, 'accessToStudent': accessToStudent, 'grades': grades, },
		context_instance=RequestContext(request))
		
def viewGrade(request, department, class_number, year, semester, section, aid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user
	
	tmpActivity = Grade.objects.select_related().get(aid=aid, uid=user.id)
	activity = percentOne(tmpActivity)
	comments = GradeComment.objects.filter(gid=activity.gid)
	
	sortGrade = Grade.objects.filter(aid=aid).order_by('mark')
	if sortGrade.count() % 2 == 1:
		median = sortGrade[(sortGrade.count()-1)/2].mark
	else:
		leftMed = sortGrade[(sortGrade.count()/2)-1].mark
		rightMed = sortGrade[(sortGrade.count()/2)].mark
		median = (leftMed + rightMed)/2
					
			
	stats = Grade.objects.filter(aid=aid).aggregate(Avg('mark'), Max('mark'), Min('mark'), Count('mark'), StdDev('mark'))
	
	accessToInst = instAccess(getInsts(class_id), getTas(class_id), user)
	accessToStudent = studentAccess(getEnrolled(class_id), user) or accessToInst
	
	return render_to_response('gradebook/viewGrade.html', {'class': c, 'accessToStudent': accessToStudent, 'activity': activity, 'comments': comments, 'stats': stats, 
'median': median },
		context_instance=RequestContext(request))
		

#Non-view Functions
def percentAll(grades):
	for grade in grades:
		tmpPercent = ((grade.mark / grade.aid.out_of) * 100)
		grade.percent = "%.2f" % tmpPercent
	return grades

def percentOne(grades):
	tmpPercent = ((grades.mark / grades.aid.out_of) * 100)
	grades.percent = "%.2f" % tmpPercent
	return grades