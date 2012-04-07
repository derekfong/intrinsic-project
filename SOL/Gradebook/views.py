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
from decimal import Decimal, getcontext
import datetime, re
from datetime import timedelta

#view that lists all the assignments
def index(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	activities = Activity.objects.filter(cid = c.cid,).order_by('due_date')
	
	#calculate aggregate grade for course
	total = {}
	total['value'] = 0
	total['out_of'] = 0
	total['percent'] = 0
	for activity in activities:
		try:
			activity.mark = Grade.objects.get(aid=activity.aid, uid = user.id).mark
			if activity.out_of > 0:
				percent = (activity.mark / activity.out_of) * 100
			else:
				percent = 0
			if activity.status == 2:
				total['value'] += percent*activity.worth/100
		except Grade.DoesNotExist:
			activity.mark = 0
			percent = 0
		if activity.status == 2:
			total['out_of'] += activity.worth
		
	if total['out_of'] > 0:
		total['percent'] = total['value'] / total['out_of']*100
			
	# content is helper function below
	content = getContent(c, user)
	content['activities'] = activities
	content['total'] = total

	return render_to_response('gradebook/index.html', content,
		context_instance=RequestContext(request))
	
#populates the page that shows assignment grade
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
		#test if student has a grade, otherwise send error
		tmpActivity = Grade.objects.get(aid=aid, uid=user.id)
		#get comments for grade
		comments = GradeComment.objects.filter(gid=tmpActivity.gid)
	except Grade.DoesNotExist:
		tmpActivity = Grade(aid=a, uid=user.userprofile, mark=0)
		comments = GradeComment.objects.filter(gid=0)
		tmpActivity.position = "N/A"
		
	#calculate percentage for mark
	activity = percentOne(tmpActivity)

	#calculate percentage for all student grades
	tmpGrade = Grade.objects.filter(aid=aid).order_by('-mark')
	
	sortGrade = percentAll(tmpGrade)

	#initialize and populate a list with count of grades
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
		
	#get classwide stats for assignment
	stats = Grade.objects.filter(aid=aid).aggregate(Avg('mark'), Max('mark'), Min('mark'), Count('mark'), StdDev('mark'))

	#calculate median grade
	if sortGrade.count() > 0:
		if sortGrade.count() % 2 == 1:
			median = sortGrade[(sortGrade.count()-1)/2].mark
		else:
			leftMed = sortGrade[(sortGrade.count()/2)-1].mark
			rightMed = sortGrade[(sortGrade.count()/2)].mark
			median = (leftMed + rightMed)/2
	else:
		message = "Assignment has no grades"
	
	#calculate position of grade compared to class
	i = 1
	prev = 0
	for grade in sortGrade:
		if tmpActivity.mark == grade.mark:
			#check last digit on position
			pos = i % 10
			if pos == 1:
				if tmpActivity.mark == prev:
					pos -= 1
					tmpActivity.position = 'T-%dth' %pos
				else:
					tmpActivity.position = '%dst' %pos
		 	elif pos == 2:
				if tmpActivity.mark == prev:
					pos -= 1
					tmpActivity.position = 'T-%dst' %pos
				else:
					tmpActivity.position = '%dnd' %pos
			elif pos == 3:
				if tmpActivity.mark == prev:
					pos -= 1
					tmpActivity.position = 'T-%dnd' %pos
				else:
					tmpActivity.position = '%drd' %pos
			else:
				if tmpActivity.mark == prev:
					pos -= 1
					if pos == 3:
						tmpActivity.position = 'T-%drd' %pos
					else:
						tmpActivity.position = 'T-%dth' %pos
				else:
					tmpActivity.position = '%dth' %pos
			#keep track of previous mark to check tie
			prev = grade.mark
		i += 1
	
	isMarked = a.status
	
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

#populates the view for grade calculator
def calculator(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	activities = Activity.objects.filter(cid = c.cid).order_by('due_date')
	
	total = {}
	total['value'] = 0
	total['out_of'] = 0
	total['percent'] = 0
	if request.method == 'POST':
		for activity in activities:
			mark_value = request.POST.__getitem__(str(activity.aid))
			if re.match("^[0-9.]+$", mark_value):
				if mark_value == '.':
					activity.mark = Decimal(0)
				else:
					activity.mark = Decimal(mark_value)
			else:
				activity.mark = Decimal(0)
			
			if activity.out_of > 0:
				percent = (activity.mark / activity.out_of) * 100
			else:
				percent = 0
			total['out_of'] += activity.worth
			if activity.out_of > 0:
				percent = (activity.mark / activity.out_of) * 100
			else:
				percent = 0
			total['value'] += percent*activity.worth/100
		if total['out_of'] > 0:
			total['percent'] = total['value'] / total['out_of']*100
	else:
		#calculate aggregate grade for course
		for activity in activities:
			try:
				if activity.status == 2:
					activity.mark = Grade.objects.get(aid=activity.aid, uid = user.id).mark
				else:
					activity.mark = 0 
			except Grade.DoesNotExist:
				activity.mark = 0
				percent = 0
			total['out_of'] += activity.worth
			if activity.out_of > 0:
				percent = (activity.mark / activity.out_of) * 100
			else:
				percent = 0
			total['value'] += percent*activity.worth/100
		if total['out_of'] > 0:
			total['percent'] = total['value'] / total['out_of']*100
			
	content = getContent(c, user)
	content['activities'] = activities
	content['total'] = total
	return render_to_response('gradebook/calculator.html', content,
		context_instance=RequestContext(request))
		
		
#Non-view Functions

# calculate percent for all grades in assignment
def percentAll(grades):
	for grade in grades:
		grade.percent = ((grade.mark / grade.aid.out_of) * 100)
	return grades

# calculate percent for a grade
def percentOne(grades):
	grades.percent = ((grades.mark / grades.aid.out_of) * 100)
	return grades

# helper function to grab the correct content
def getContent(c, user):
	latestAnnouncements = getAnnouncements(c.cid)
	for announce in latestAnnouncements:
		if (datetime.datetime.now() - announce.date_posted) < timedelta(days=1):
			announce.isNew = 1
		else:
			announce.isNew = 0
	content = {'class': c , 'accessToInst': instAccess(getInsts(c.cid), getTas(c.cid), user), 
		'accessToStudent': studentAccess(getEnrolled(c.cid), user), 'latestAnnouncements': latestAnnouncements, 
		'classUrl': getClassUrl(c), 'class_list': getClassList(user), 'isCurrent': checkCurrent(c) }
	return content
	