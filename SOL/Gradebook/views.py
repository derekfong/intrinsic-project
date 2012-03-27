from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from Main.models import Course
from Gradebook.models import Grade, GradeComment
from Instructor.models import Activity, Announcement
from Instructor.views import getClassUrl
from Student.views import instAccess, studentAccess, getInsts, getTas, getEnrolled, getAnnouncements, checkCurrent, currentSemester
from django.db.models import Avg, Max, Min, Count, StdDev
import datetime
#from chartit import DataPool, Chart

# Create your views here.

def index(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user
	
	accessToInst = instAccess(getInsts(class_id), getTas(class_id), user)
	accessToStudent = studentAccess(getEnrolled(class_id), user) 
	isCurrent = checkCurrent(c)
	
	latestAnnouncements = getAnnouncements(class_id)
	
	tmpGrades = Grade.objects.filter(aid__cid=class_id, uid=user.id)
	grades = percentAll(tmpGrades)
	
	activities = Activity.objects.filter(cid = class_id)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)

	content = {'class': c, 'activities': activities,'accessToStudent': accessToStudent, 'accessToInst': accessToInst, 'grades': grades, 
	'latestAnnouncements': latestAnnouncements, 'classUrl': getClassUrl(c), 'class_list': class_list, 'isCurrent': isCurrent}
	return render_to_response('gradebook/index.html', content,
		context_instance=RequestContext(request))
		
def viewGrade(request, department, class_number, year, semester, section, aid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	a = get_object_or_404(Activity, pk=aid)
	user = request.user
	
	accessToInst = instAccess(getInsts(class_id), getTas(class_id), user)
	isCurrent = checkCurrent(c)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
	activity = []
	comments = []
	stats = []
	median = 0
	barChart = []
	message = ''
	isMarked = 0
	##### NEEDS FIXING: When no grade for student, must output 0. ############## 
	try:
		tmpActivity = Grade.objects.get(aid=aid, uid=user.id)
		activity = percentOne(tmpActivity)
		comments = GradeComment.objects.filter(gid=activity.gid)
		tmpGrade = Grade.objects.filter(aid=aid)
		sortGrade = percentAll(tmpGrade)
		barChart = [0,0,0,0,0,0,0,0,0,0,0]
		for aGrade in sortGrade:
			if aGrade.percent < 10:
				barChart[0] += 1
			elif aGrade.percent < 20:
				barChart[1] += 1
			elif aGrade.percent < 30:
				barChart[2] += 1
			elif aGrade.percent < 40:
				barChart[3] += 1
			elif aGrade.percent < 50:
				barChart[4] += 1
			elif aGrade.percent < 60:
				barChart[5] += 1
			elif aGrade.percent < 70:
				barChart[6] += 1
			elif aGrade.percent < 80:
				barChart[7] += 1
			elif aGrade.percent < 90:
				barChart[8] += 1
			elif aGrade.percent < 100:
				barChart[9] += 1
			else:
				barChart[10] += 1
		stats = Grade.objects.filter(aid=aid).aggregate(Avg('mark'), Max('mark'), Min('mark'), Count('mark'), StdDev('mark'))
		if sortGrade.count() % 2 == 1:
			median = sortGrade[(sortGrade.count()-1)/2].mark
		else:
			leftMed = sortGrade[(sortGrade.count()/2)-1].mark
			rightMed = sortGrade[(sortGrade.count()/2)].mark
			median = (leftMed + rightMed)/2
		isMarked = a.status
	except Grade.DoesNotExist:
		message = 'Assignment has not been graded'
	
	latestAnnouncements = getAnnouncements(class_id)
	
	accessToInst = instAccess(getInsts(class_id), getTas(class_id), user)
	accessToStudent = studentAccess(getEnrolled(class_id), user) or accessToInst
	
	content = {'class': c, 'accessToStudent': accessToStudent, 'activity': activity, 'latestAnnouncements': latestAnnouncements, 
	'comments': comments, 'stats': stats, 'median': median, 'barChart': barChart, 'accessToInst': accessToInst, 'classUrl': getClassUrl(c), 
	'messsage': message, 'isMarked': isMarked, 'class_list': class_list, 'isCurrent': isCurrent}
	return render_to_response('gradebook/viewGrade.html', content,
		context_instance=RequestContext(request))
		
#Non-view Functions
def percentAll(grades):
	for grade in grades:
		grade.percent = ((grade.mark / grade.aid.out_of) * 100)
		#grade.percent = "%.2f" % tmpPercent
	return grades

def percentOne(grades):
	grades.percent = ((grades.mark / grades.aid.out_of) * 100)
	#grades.percent = "%.2f" % tmpPercent
	return grades