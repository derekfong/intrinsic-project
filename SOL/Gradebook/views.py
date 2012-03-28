from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib import auth
from Main.models import Course
from Gradebook.models import Grade, GradeComment
from Instructor.models import Activity, Announcement
from Instructor.views import getClassUrl
from Student.views import instAccess, studentAccess, getInsts, getTas, getEnrolled, getAnnouncements, checkCurrent, currentSemester, getClassList, getClassObject
from django.db.models import Avg, Max, Min, Count, StdDev
import datetime
#from chartit import DataPool, Chart

# Create your views here.

def index(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)

	tmpGrades = Grade.objects.filter(aid__cid=c.cid, uid=user.id)
	grades = percentAll(tmpGrades)
	
	activities = Activity.objects.filter(cid = c.cid)
	
	content = getContent(c, user)
	content['activities'] = activities
	content['grades'] = grades

	return render_to_response('gradebook/index.html', content,
		context_instance=RequestContext(request))
		
def viewGrade(request, department, class_number, year, semester, section, aid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	a = get_object_or_404(Activity, pk=aid)
	
	activity = []
	comments = []
	stats = []
	median = 0
	barChart = []
	message = ''
	isMarked = 0
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
	
	content = getContent(c, user)
	content['activity'] = activity
	content['comments'] = comments
	content['stats'] = stats
	content['median'] = median
	content['barChart'] = barChart
	content['isMarked'] = isMarked
	content['message'] = message
	
	return render_to_response('gradebook/viewGrade.html', content,
		context_instance=RequestContext(request))
		
#Non-view Functions
def percentAll(grades):
	for grade in grades:
		grade.percent = ((grade.mark / grade.aid.out_of) * 100)
	return grades

def percentOne(grades):
	grades.percent = ((grades.mark / grades.aid.out_of) * 100)
	return grades

def getContent(c, user):
	content = {'class': c , 'accessToInst': instAccess(getInsts(c.cid), getTas(c.cid), user), 
		'accessToStudent': studentAccess(getEnrolled(c.cid), user), 'latestAnnouncements': getAnnouncements(c.cid), 
		'classUrl': getClassUrl(c), 'class_list': getClassList(user), 'isCurrent': checkCurrent(c) }
	return content