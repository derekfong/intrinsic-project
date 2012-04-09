from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.template import RequestContext
from Main.models import Course, ClassList, UserProfile
from django.contrib.auth.models import User
from Instructor.models import Activity, Announcement, CourseContent, Slide, Greeting, Quiz, QuizQuestion
from Main.views import currentSemester
from Student.models import Submission, QuizAttempt, QuizResult
from Gradebook.models import Grade
from Student.forms import SubmissionForm
#from reportlab.pdfgen import canvas
from django.http import HttpResponse, HttpResponseRedirect
import datetime, os
from datetime import timedelta
	
# Create your views here.
def index(request, department, class_number, year, semester, section):
	# gets corresponding classes to display on the website
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	nextWeek = datetime.datetime.now()+timedelta(days=14)

	upcomingActivity = Activity.objects.filter(due_date__lte = nextWeek, due_date__gte = datetime.datetime.now(), cid=c.cid).order_by('due_date')
	
	try: 
		greeting = Greeting.objects.get(cid=c.cid).message
	except Greeting.DoesNotExist:
		greeting = "I would like to welcome you all to "+c.department+" "+c.class_number+".  I look forward to this semester and I hope you all have fun and enjoy."
		
	content = getContent(c, user)
	content['upcomingActivity'] = upcomingActivity
	content['greeting'] = greeting
	
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

# View that allows a student to submit a file for an activity.
def activities_submit(request, department, class_number, year, semester, section, aid):
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

	accessToStudent = studentAccess(enrolled, user)
	accessToInst = instAccess(instructors, tas, user)
	isCurrent = checkCurrent(c)
	
	submissions = Submission.objects.filter(aid=aid, uid=user.id).order_by('-submit_date')
	
	for submission in submissions:
		submission.filename = os.path.basename(submission.file_path.path)
	
	activity = Activity.objects.get(aid=aid)
	message = ''
	
	if request.method == 'POST':
		form = SubmissionForm(request.POST, request.FILES)
		if form.is_valid():
			user_profile = UserProfile.objects.get(user=request.user)
			num_of_submits = Submission.objects.filter(aid=aid, uid=user_profile.id).count()	
			activity = Submission(aid=activity, uid=user_profile, submit_number=num_of_submits+1)
			submitted_file = request.FILES['file_path']
			activity.file_path.save(submitted_file.name, submitted_file)
			activity = Activity.objects.get(aid=aid)
			message = 'You have successfully submitted your file'
	else:
		form = SubmissionForm()
	
	content = {'accessToStudent': accessToStudent, 'accessToInst': accessToInst, 'class': c, 'activity': activity, 'submissions': submissions, 'message': message, 'form': form,
	'classUrl': getClassUrl(c), 'class_list': class_list, 'isCurrent': isCurrent}
	return render_to_response('student/submission.html', content, 
		context_instance=RequestContext(request))

def quiz(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	now = datetime.datetime.now()
	quizzes = Quiz.objects.filter(cid=c.cid)
	for quiz in quizzes:
		quiz.attempts = QuizAttempt.objects.filter(qid=quiz.id, uid=user.id).count()
		if quiz.start_date <= now and quiz.end_date >= now:
			quiz.current = 1
		else:
			quiz.current = 0
	
	content = getContent(c, user)
	content["quizzes"] = quizzes
		
	return render_to_response('student/quiz.html', content, 
		context_instance=RequestContext(request))
	
def quizTake(request, department, class_number, year, semester, section, qid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	q = get_object_or_404(Quiz, pk=qid)
	now = datetime.datetime.now()
	
	if q.start_date <= now and q.end_date >= now:
		q.current = 1
	else:
		q.current = 0
	
	attempts = QuizAttempt.objects.filter(qid=q.id, uid=user.id)
	
	questions = QuizQuestion.objects.filter(qid=q.id)
	
	message = ''
	if request.method == "POST":
		finalMark = 0
		try: 
			answers = []
			for question in questions:
				question.guess = int(request.POST.__getitem__(str(question.id)))
				answer = question.answer
				if question.guess == answer:
					question.result = 1
					finalMark += 1
				else:
					question.result = 0
			attempt = QuizAttempt(qid=q, uid=user.userprofile, time=datetime.datetime.now(), result=finalMark)
			attempt.save()

			for question in questions:
				qObj = QuizQuestion.objects.get(id=question.id)
				QuizResult(attempt=attempt, question=qObj, guess=question.guess).save()
			
			content = getContent(c, user)
			content["quiz"] = q
			content["questions"]=questions
			content["finalMark"] = finalMark

			return render_to_response('student/quizResult.html', content, 
				context_instance=RequestContext(request))
				
		except KeyError:
			message = 'You need to answer all questions'

	
	content = getContent(c, user)
	
	content["quiz"] = q
	content["questions"]=questions
	content["message"] = message
	content["attempts"] = attempts
		
	return render_to_response('student/quizTake.html', content, 
		context_instance=RequestContext(request))
		
def quizResults(request, department, class_number, year, semester, section, qid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	q = get_object_or_404(Quiz, pk=qid)
	
	attempts = QuizAttempt.objects.filter(qid=q.id, uid=user.id)
	for attempt in attempts:
		attempt.results = QuizResult.objects.filter(attempt=attempt.id)
		attempt.out_of = attempt.results.count()
		for result in attempt.results:
			if result.guess == result.question.answer:
				result.result = 1
			else:
				result.result = 0

	content = getContent(c, user)
	content["attempts"] = attempts
	content["quiz"] = q

	return render_to_response('student/quizAttempts.html', content, 
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
	return Course.objects.filter(classlist__uid=user.id, year=year, semester=semester).order_by('department', 'class_number')
	
def getClassObject(department, class_number, year, semester, section, user):
	try:
		class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	except Course.DoesNotExist:
		raise  Http404

	return get_object_or_404(Course, pk=class_id)


# actually display content on the main page relating to the student user
def getContent(c, user):
	instructors = getInsts(c.cid)
	tas = getTas(c.cid)
	students = getStudents(c.cid)
	enrolled = getEnrolled(c.cid)
	latestAnnouncements = getAnnouncements(c.cid)
	for announce in latestAnnouncements:
		if (datetime.datetime.now() - announce.date_posted) < timedelta(days=1):
			announce.isNew = 1
		else:
			announce.isNew = 0

	content = {'class': c , 'instructors': instructors, 
		'tas': tas, 'students': students, 'accessToInst': instAccess(instructors, tas, user), 
		'accessToStudent': studentAccess(enrolled, user), 'latestAnnouncements': latestAnnouncements, 'classUrl': getClassUrl(c), 
		'class_list': getClassList(user), 'isCurrent': checkCurrent(c), }
	return content
