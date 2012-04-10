from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404
from django.template import RequestContext, Context
from Main.models import Course, ClassList, UserProfile
from django.contrib.auth.models import User
from Instructor.models import Activity, Announcement, CourseContent, Slide, Greeting, Quiz, QuizQuestion
from Main.views import currentSemester
from Student.models import Submission, QuizAttempt, QuizResult
from Gradebook.models import Grade
from Student.forms import SubmissionForm
from django.http import HttpResponse, HttpResponseRedirect
import datetime, os
from datetime import timedelta
from django_xhtml2pdf.utils import generate_pdf
	
#Initial view for students
def index(request, department, class_number, year, semester, section):
	# gets corresponding classes to display on the website
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	#Gets all the activites coming up in the next 7 days 
	nextWeek = datetime.datetime.now()+timedelta(days=7)
	upcomingActivity = Activity.objects.filter(due_date__lte = nextWeek, due_date__gte = datetime.datetime.now(), cid=c.cid).order_by('due_date')
	
	#Check if greeting exists, otherwise display generic welcome message
	try: 
		greeting = Greeting.objects.get(cid=c.cid).message
	except Greeting.DoesNotExist:
		greeting = "I would like to welcome you all to "+c.department+" "+c.class_number+".  I look forward to this semester and I hope you all have fun and enjoy."
		
	content = getContent(c, user)
	content['upcomingActivity'] = upcomingActivity
	content['greeting'] = greeting
	
	return render_to_response('student/index.html', content,
		context_instance=RequestContext(request))

#View to display syllabus		
def syllabus(request, department, class_number, year, semester, section):
	# grab corresponding syllabus for that class
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
		
	message = ''
	#Check if a syllabus has been created
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

#View to download Syllabus as PDF		
def downloadSyllabus(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)

	message = ''
	#Check if syllabus exists
	try:
		syllabus = CourseContent.objects.get(cid = c.cid)
	except CourseContent.DoesNotExist:
		message = 'No syllabus has been created for this class.'
		syllabus = []

	content = getContent(c, user)
	content['syllabus'] = syllabus
	content['message'] = message
	filename = c.department+'%s'%c.class_number+'%s'%year+'.pdf'
	resp = HttpResponse(content_type='application/pdf')
	resp['Content-Disposition'] = 'attachment; filename='+filename.lower()
	result = generate_pdf('student/syllabusPDF.html', file_object=resp, context=content)
	return result

#Displays slides to students
def slides(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
		
	slides = Slide.objects.filter(cid = c.cid)

	content = getContent(c, user)
	content['slides'] = slides

	return render_to_response('student/slides.html', content, 
		context_instance=RequestContext(request))
	
#Displayed Activities and allows students to submit assignments
def activities(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	activities = Activity.objects.filter(cid=c.cid).order_by('due_date')
	for activity in activities:
		activity.pastDue = pastDue(activity)
	
	content = getContent(c, user)
	content['activities'] = activities
	
	return render_to_response('student/activities.html', content, 
		context_instance=RequestContext(request))

#View that allows a student to submit a file for an activity.
def activities_submit(request, department, class_number, year, semester, section, aid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	activity = get_object_or_404(Activity, pk=aid)
	user = request.user
	
	submissions = Submission.objects.filter(aid=aid, uid=user.id).order_by('-submit_date')
	
	for submission in submissions:
		submission.filename = os.path.basename(submission.file_path.path)
	
	message = ''
	error_message = ''
	form = ''
	
	if datetime.datetime.now() <= activity.due_date:
		if 'No Submission' == activity.submission_file_type:
			error_message = "No submission necessary for "+ activity.activity_name
		else:
			if request.method == 'POST':
				form = SubmissionForm(request.POST, request.FILES)
				if form.is_valid():
					# Verify file type and size (8MB max)
					uploaded_file = request.FILES['file_path']
					max_file_size = 16777216
					file_types_allowed = [activity.submission_file_type,]
					isProperFileType = checkFileType(uploaded_file, file_types_allowed)
					isProperFileSize = checkFileSize(uploaded_file, max_file_size)
					if isProperFileType and isProperFileSize:	
						num_of_submits = Submission.objects.filter(aid=aid, uid=user.userprofile.id).count()	
						submit_activity = Submission(aid=activity, uid=user.userprofile, submit_number=num_of_submits+1)
						submitted_file = request.FILES['file_path']
						submit_activity.file_path.save(submitted_file.name, submitted_file)
						message = 'You have successfully submitted your file'
					elif not isProperFileType:
						error_message = "Error: File type is incorrect - must be "+ activity.submission_file_type
					elif not isProperFileSize:
						error_message = "Error: File size exceeds the max of 8MB"
			else:
				form = SubmissionForm()
	else:
		error_message = 'The due date ('+ activity.due_date.strftime("%B %d, %Y %I:%M%p") +') has passed for '+ activity.activity_name
	
	content = getContent(c, user)
	content['form'] = form
	content['activity'] = activity
	content['submissions'] = submissions
	content['message'] = message
	content['error_message'] = error_message
	return render_to_response('student/submission.html', content, 
		context_instance=RequestContext(request))

#Displays Quizzes available to student
def quiz(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	now = datetime.datetime.now()
	quizzes = Quiz.objects.filter(cid=c.cid)
	for quiz in quizzes:
		#Number of attempts on quiz for student
		quiz.attempts = QuizAttempt.objects.filter(qid=quiz.id, uid=user.id).count()
		
		#Quiz is current if within start and end date
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
	
	#Quiz is current if within start and end date
	if q.start_date <= now and q.end_date >= now:
		q.current = 1
	else:
		q.current = 0
	
	#Number of attempts on quiz for student
	attempts = QuizAttempt.objects.filter(qid=q.id, uid=user.id)
	
	#Gets all quiz questions
	questions = QuizQuestion.objects.filter(qid=q.id)
	
	message = ''
	#Grade the quiz and return the results to the students
	if request.method == "POST":
		finalMark = 0
		#Make sure student has answered all questions
		try: 
			answers = []
			for question in questions:
				#Gets the students guess for the question
				question.guess = int(request.POST.__getitem__(str(question.id)))
				answer = question.answer
				#Final Mark is incremented if student gets it right
				if question.guess == answer:
					question.result = 1
					finalMark += 1
				else:
					question.result = 0
			#Commits a quiz attempt to database
			attempt = QuizAttempt(qid=q, uid=user.userprofile, time=datetime.datetime.now(), result=finalMark)
			attempt.save()

			#Commits a quiz result for each question answered to database
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
		
#Shows the results for all attempts at a quiz
def quizResults(request, department, class_number, year, semester, section, qid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	q = get_object_or_404(Quiz, pk=qid)
	
	#Gets all the student's attempts at the quiz
	attempts = QuizAttempt.objects.filter(qid=q.id, uid=user.id)
	for attempt in attempts:
		#Gets all the student's results for each attempt
		attempt.results = QuizResult.objects.filter(attempt=attempt.id)
		#Gets the max mark for quiz
		attempt.out_of = attempt.results.count()
		#Check if student got each question right
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

#Displays all the announcements
def announcements(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)

	#Get all announcements for class
	announcements = Announcement.objects.filter(cid=c.cid).order_by('-date_posted')

	content = getContent(c, user)
	content['announcements'] = announcements
	
	return render_to_response('student/announcements.html', content, 
		context_instance=RequestContext(request))			
		
#Gets the 3 newest announcements for a given course and truncate them if too long
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
	
#Check to make sure an activity isn't past the due date
def pastDue(activity):
	if datetime.datetime.now() > activity.due_date:
		return 1
	else:
		return 0

#Check if there is permission as instructor/marker
def instAccess(instructors, tas, user):
	for ta in tas:
		if user.id == ta.user.id:
			return 1
	for instructor in instructors:
		if user.id == instructor.user.id:
			return 1
	return 0

#Check if there is permission as student.
def studentAccess(students, user):
	for student in students:
		if user.id == student.user.id:
			return 1
	return 0


#Gets Instructors, TAs, Students, Enrolled Accounts
def getInsts(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id, classlist__is_instructor=1)

def getTas(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id, classlist__is_ta=1)

def getStudents(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id, classlist__is_ta=0, classlist__is_instructor=0).order_by('user__last_name', 'user__first_name', 'sfu_id')
	
def getEnrolled(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id)

#Get class URL		
def getClassUrl(c):
	classUrl = '/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/'
	return classUrl
	
#Check if a class is current (offered in current semester)
def checkCurrent(c):
	year = datetime.date.today().year
	semester = currentSemester()
	
	if year == c.year and semester == c.semester:
		return 1
	else:
		return 0

#Gets all current classes student is enrolled in	
def getClassList(user):
	year = datetime.date.today().year
	semester = currentSemester()
	return Course.objects.filter(classlist__uid=user.id, year=year, semester=semester).order_by('department', 'class_number')

#Get class object if it exists, otherwise return a 404	
def getClassObject(department, class_number, year, semester, section, user):
	try:
		class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	except Course.DoesNotExist:
		raise  Http404

	return get_object_or_404(Course, pk=class_id)

#Sets all the generic contexts to send to template
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
