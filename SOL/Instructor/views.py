from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from Main.models import Course, ClassList
from Main.views import checkFileType, checkFileSize
from Instructor.models import Announcement, Activity, CourseContent, Slide, Greeting, Quiz, QuizQuestion
from Gradebook.models import Grade, UploadGrade, DownloadGrade, OnlineGrade
from Calendar.models import Event, Label
from Calendar.views import getClassLabel
from Student.models import Submission
from Student.views import instAccess, getInsts, getTas, getStudents, getClassUrl, getEnrolled, studentAccess, getAnnouncements, currentSemester, getClassObject, getClassList, QuizAttempt
from forms import AnnounceForm, ActivityForm, CourseForm, GradeForm, SlideForm, GreetingsForm, QuizForm
from decimal import Decimal, getcontext
from django.forms.models import modelformset_factory
from django.forms.formsets import formset_factory
from django.contrib.auth.models import User
from Main.models import UserProfile
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Max
import datetime, xlrd, xlwt, re, zipfile, os, time
from django import forms
from datetime import timedelta

#View to generate the page for the main view of Instructor App
def index(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	content = getContent(c, user)
	return render_to_response('instructor/index.html', content,
		context_instance=RequestContext(request))

#Lets the instructor add a greeting for the main class view
def greeting(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	message = ''
	classUrl = getClassUrl(c)
	
	#Updates the greeting
	if request.method == 'POST':
		greeting = Greeting(cid=c)
		form = GreetingsForm(request.POST, instance=greeting)
		if form.is_valid():
			try:
				Greeting.objects.get(cid=c.cid)
				update = Greeting.objects.filter(cid=c.cid).update(message=form.cleaned_data["message"])
			except Greeting.DoesNotExist:
				form.save()
			message = 'You have successfully updated the course greeting.'
	else:
		#Initializes the form if a custom message exists, otherwise uses generic message.
		try:
			greet = Greeting.objects.get(cid=c.cid)
			form = GreetingsForm(initial={'message': greet.message,})
		except Greeting.DoesNotExist:
			greet = "I would like to welcome you all to "+c.department+" "+c.class_number+".  I look forward to this semester and I hope you all have fun and enjoy."
			form = GreetingsForm(initial={'message': greet,})
	
	content = getContent(c, user)
	content['form'] = form
	content['classUrl'] = classUrl
	content['message'] = message
	return render_to_response('instructor/greeting.html', content, 
		context_instance=RequestContext(request))

#View to generate the page for the syllabus view of Instructor App
def syllabus(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	message = ''
	classUrl = getClassUrl(c)

	#Form that has defined fields for prof to fill out to create a syllabus
	if request.method == 'POST':
		content = CourseContent(cid=c, created_on=datetime.datetime.now(), was_updated=0, updated_on=datetime.datetime.now() )
		form = CourseForm(request.POST, instance=content)
		if form.is_valid():
			form.save()
			message = 'You have successfully created a syllabus'
	else:
		#If form exists, redirect to update page, otherwise send blank form
		try:
			course = CourseContent.objects.get(cid=c.cid)
			return HttpResponseRedirect(classUrl+"instructor/syllabus/update/%s" %course.id)
		except CourseContent.DoesNotExist:
			form = CourseForm()
	
	content = getContent(c, user)
	content['form'] = form
	content['message'] = message
	return render_to_response('instructor/syllabus.html', content, 
		context_instance=RequestContext(request))

#View to update the graded syllabus in the Instructor App
def updateSyllabus(request, department, class_number, year, semester, section, sid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	s = get_object_or_404(CourseContent, pk=sid)
	
	message = ''
	classUrl = getClassUrl(c)
	#Updates the syllabus
	if request.method == 'POST':
		course = CourseContent(id=sid, cid=c, created_on=s.created_on, was_updated=1, updated_on=datetime.datetime.now() )
		form = CourseForm(request.POST, instance=course)
		if form.is_valid():
			form.save()
			message = 'You have successfully updated the syllabus'
	else:
		#Initializes the form with existing syllabus information
		course = CourseContent.objects.get(cid=c.cid)
		form = CourseForm(initial={'officeHrs': course.officeHrs, 'officeLocation': course.officeLocation, 'phoneNumber': course.phoneNumber, 'TaOfficeLocation': course.TaOfficeLocation, 'TaOfficeHrs': course.TaOfficeHrs, 'lectTime': course.lectTime, 'prereq': course.prereq, 'books': course.books, 'topics': course.topics, 'markingScheme': course.markingScheme, 'academicHonesty': course.academicHonesty, 'additionalInfo': course.additionalInfo,})
	
	content = getContent(c, user)
	content['form'] = form
	content['classUrl'] = classUrl
	content['message'] = message
	return render_to_response('instructor/syllabus.html', content, 
		context_instance=RequestContext(request))

#Allows the instructor to add lecture slides
def slides(request, department, class_number, year, semester, section):
	# slides are just lecture notes
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	error_message = ''
	slides = Slide.objects.filter(cid=c.cid)
	
	#Uploads the slide file and adds to database
	if request.method == 'POST':
		slide = Slide(cid=c, uploaded_on=datetime.datetime.now())
		form = SlideForm(request.POST, request.FILES, instance=slide)
		if form.is_valid():
			# Verify file type and size (8MB max)
			uploaded_file = request.FILES['file_path']
			max_file_size = 16777216
			file_types_allowed = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.txt', '.zip']
			isProperFileType = checkFileType(uploaded_file, file_types_allowed)
			isProperFileSize = checkFileSize(uploaded_file, max_file_size)
			if isProperFileType and isProperFileSize:
				submit_slide = Slide(cid=c, title=form.cleaned_data['title'], uploaded_on=datetime.datetime.now())
				submitted_file = request.FILES['file_path']
				submit_slide.file_path.save(submitted_file.name, submitted_file)
				return HttpResponseRedirect("")
			elif not isProperFileType:
				error_message = "Error: File type is incorrect - must be one of .pdf, .doc, .docx, .ppt, .pptx, .txt, or .zip"
			elif not isProperFileSize:
				error_message = "Error: File size exceeds the max of 8MB"
	else:
		form = SlideForm()
		
	content = getContent(c, user)
	content['form'] = form
	content['slides'] = slides
	content['error_message'] = error_message
	return render_to_response('instructor/slides.html', content, 
		context_instance=RequestContext(request))
	
#Updates the slides
def updateSlides(request, department, class_number, year, semester, section, slid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	#Makes sure the slide exists, otherwise return 404
	s = get_object_or_404(Slide, pk=slid)

	slides = Slide.objects.filter(cid=c.cid)
	
	classUrl = getClassUrl(c)
	#Updates the slide file and in the database
	if request.method == 'POST':
		slide = Slide(cid=c, uploaded_on=datetime.datetime.now(), id=slid)
		form = SlideForm(request.POST, request.FILES, instance=slide)
		if form.is_valid():
			form.save()
			url = classUrl +'instructor/slides'
			return HttpResponseRedirect(url)
	else:
		#Initializes the form
		form = SlideForm(initial={'title': s.title, 'file_path': s.file_path})
	
	content = getContent(c, user)
	content['form'] = form
	content['slides'] = slides
	return render_to_response('instructor/slides.html', content, 
		context_instance=RequestContext(request))
		
#Deletes the slide from the database
def removeSlides(request, department, class_number, year, semester, section, slid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	#Makes sure the slide exists, otherwise return 404
	s = get_object_or_404(Slide, pk=slid)
	accessToInst = instAccess(getInsts(c.cid), getTas(c.cid), user)

	classUrl = getClassUrl(c)
	if accessToInst:
		slide = Slide.objects.get(id=slid)
		slide.delete()
		url = classUrl + 'instructor/slides'
		return HttpResponseRedirect(url)
	else:
		content = {'accessToInst': accessToInst, 'classUrl': classUrl}
		return render_to_response('instructor/slides.html', content, 
			context_instance=RequestContext(request))
			
#View to generate the page for the graded activities view of Instructor App
def activity(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	#Gets the list of students for want to receive email notifications for graded activities
	emailStudents = UserProfile.objects.filter(classlist__cid=c.cid, setting__email_activity=1)

	activities = Activity.objects.filter(cid=c.cid).order_by('due_date')
	
	if request.method == 'POST':
		activity = Activity(cid=c, released=0)
		form = ActivityForm(request.POST, request.FILES, instance=activity)
		if form.is_valid():
			if form.cleaned_data['status'] == 2:
				form.cleaned_data["released"] = 1
			else:
				form.cleaned_data["released"] = 0
			form.save()
			
			#Create a calendar event for each activity created
			label = getClassLabel(user, c.cid, department, class_number)
			event_name = form.cleaned_data['activity_name']
			date = form.cleaned_data['due_date']
			description = form.cleaned_data['description']
			
			
			event = Event(uid=request.user.userprofile, cid=c.cid, lid=label, event_name=event_name, date=date, description=description)
			event.save()
			
			#If grade has been released by instructor/TA
			if form.cleaned_data['status'] == 2:
				#Generate+send email announcement
				subject = c.department+' %s' %c.class_number+': Grade released for '+form.cleaned_data['activity_name']
				from_email = 'itsatme@gmail.com'
				to = []
				for student in emailStudents:
					to.append(student.user.email)
				html_content = render_to_string('instructor/emailActivityTemplate.html', {'class': c, 'activity': activity,})
				text_content = strip_tags(html_content)
				msg = EmailMultiAlternatives(subject, text_content, from_email, to)
				msg.attach_alternative(html_content, "text/html")
				msg.send()
				
				#Created announcement for it
				title = 'Grade released for '+form.cleaned_data['activity_name']
				content = "A new grade was released for "+form.cleaned_data['activity_name']
				act = Announcement(uid=user.userprofile, title=title, content=content, date_posted=datetime.datetime.now(), cid=c, send_email=0, was_updated=0, updated_by=user.userprofile, updated_on=datetime.datetime.now())
				act.save()
			return HttpResponseRedirect("")
	else:
		form = ActivityForm()
	
	content = getContent(c, user)
	content['form'] = form
	content['activities'] = activities
	content['update'] = 0
	return render_to_response('instructor/activity.html', content, 
		context_instance=RequestContext(request))
		
#View to update the graded activity in the Instructor App
def updateActivity(request, department, class_number, year, semester, section, aid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	a = get_object_or_404(Activity, pk=aid)

	#Gets all students who wish to receive email when assignment is released
	emailStudents = UserProfile.objects.filter(classlist__cid=c.cid, setting__email_activity=1)
	activities = Activity.objects.filter(cid=c.cid)
	
	if request.method == 'POST':
		activity = Activity(cid=c, aid=aid, released=0)
		form = ActivityForm(request.POST, request.FILES, instance=activity)
		if form.is_valid():
			form.save()
			if form.cleaned_data['status'] == 2:
				rel = 1
			else:
				rel = 0
			Activity.objects.filter(aid=a.aid).update(released=rel)
			
			#Update the calendar event for the activity
			event = Event.objects.get(uid=request.user.userprofile, cid=c.cid, event_name=a.activity_name)
			event.date = form.cleaned_data['due_date']
			event.description = form.cleaned_data['description']
			event.name = form.cleaned_data['activity_name']
			event.save()
			
			if form.cleaned_data['status'] == 2 and a.released == 0:
				#Generate+send email announcement
				subject = c.department+' %s' %c.class_number+': Grade released for '+form.cleaned_data['activity_name']
				from_email = 'itsatme@gmail.com'
				to = []
				for student in emailStudents:
					to.append(student.user.email)
				html_content = render_to_string('instructor/emailActivityTemplate.html', {'class': c, 'act_name': form.cleaned_data['activity_name'], 'act_aid': aid})
				text_content = strip_tags(html_content)
				msg = EmailMultiAlternatives(subject, text_content, from_email, to)
				msg.attach_alternative(html_content, "text/html")
				msg.send()
				
				#Created announcement for it
				title = 'Grade released for '+form.cleaned_data['activity_name']
				content = "A new grade was released for "+form.cleaned_data['activity_name']
				act = Announcement(uid=user.userprofile, title=title, content=content, date_posted=datetime.datetime.now(), cid=c, send_email=0, was_updated=0, updated_by=user.userprofile, updated_on=datetime.datetime.now())
				act.save()
			url = getClassUrl(c) + 'instructor/activity'
			return HttpResponseRedirect(url)
	else:
		tmp = Activity.objects.get(aid=aid)
		form = ActivityForm(initial={'activity_name': tmp.activity_name, 'out_of': tmp.out_of, 'worth': tmp.worth, 'description': tmp.description, 'submission_file_type': tmp.submission_file_type, 'description_doc': tmp.description_doc, 'due_date': tmp.due_date, 'status': tmp.status, })

	content = getContent(c, user)
	content['form'] = form
	content['activities'] = activities
	content['update'] = 1
	return render_to_response('instructor/activity.html', content, 
		context_instance=RequestContext(request))
		
#View to delete the graded activity in the Instructor App
def removeActivity(request, department, class_number, year, semester, section, aid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	a = get_object_or_404(Activity, pk=aid)

	accessToInst = instAccess(getInsts(c.cid), getTas(c.cid), user)

	if accessToInst:
		#Remove the calendar event for the activity
		try: 
			event = Event.objects.get(uid=request.user.userprofile, cid=c.cid, event_name=a.activity_name)
			event.delete()
		except:
			event = ''
		
		activity = Activity.objects.get(aid=aid)
		activity.delete()
		url = getClassUrl(c) + 'instructor/activity'
		return HttpResponseRedirect(url)
	else:
		content = {'accessToInst': accessToInst, 'classUrl': getClassUrl(c)}
		return render_to_response('instructor/announcement.html', content, 
			context_instance=RequestContext(request))

# View that retrieves all the most recent submissions from each student. Returns as a zip.
def getSubmissions(request, department, class_number, year, semester, section, aid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	a = get_object_or_404(Activity, pk=aid)

	user = request.user
	
	activity_name = a.activity_name
	
	# Establish a zip file of all submission for the activity
	#class_folder = '/var/www/intrinsic-project/SOL/media/submissions/%s' %year +'/'+ semester +'/'+ department +'/'+ class_number +'/'+ section +'/'
	class_folder = '/Users/kevin/Dropbox/intrinsic-project Apr10/SOL/media/submissions/%s' %year +'/'+ semester +'/'+ department +'/'+ class_number +'/'+ section +'/'
	#class_folder = '/Users/derek/Desktop/LOCAL/intrinsic-project/SOL/media/submissions/%s' %year +'/'+ semester +'/'+ department +'/'+ class_number +'/'+ section +'/'
	
	zip_name = activity_name + '.zip'
	activity_zip = zipfile.ZipFile(class_folder + zip_name, 'w')

	activity_folder = class_folder +'/'+ activity_name +'/'
	
	class_list = getStudents(class_id)
	activity_submissions = Submission.objects.filter(aid=aid)
	
	# Go through all the students in the class and retrieve the latest submission
	for student in class_list:
		student_folder = User.objects.get(id=student.id).username
		last_submit = activity_submissions.filter(uid=student.id).count()
		if last_submit > 0:
			latest_submission = activity_submissions.filter(uid=student.id, submit_number=last_submit).get()
			submission_file = latest_submission.file_path.path
			file_extension = os.path.splitext(os.path.basename(submission_file))
			activity_zip.write(submission_file, activity_name +'/'+ student_folder +'/'+ activity_name + file_extension[1])
	
	# Close and create the zip file of submissions for the activity
	activity_zip.close()
	
	file_to_send = file(class_folder + zip_name)
	
	response = HttpResponse(file_to_send, content_type='application/zip')
	response['Content-Disposition'] = 'attachment; filename='+zip_name
	return response

#View to generate the page for the announcements view of Instructor App	
def announcement(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)

	#Gets all students who wish to receive email when assignment is released
	emailStudents = UserProfile.objects.filter(classlist__cid=c.cid, setting__email_announcement=1)
	announcements = Announcement.objects.filter(cid=c.cid).order_by('-date_posted')

	if request.method == 'POST':
		announce = Announcement(cid=c, uid=user.userprofile, was_updated=0, updated_on=datetime.datetime.now(), updated_by=user.userprofile, date_posted=datetime.datetime.now())
		form = AnnounceForm(request.POST, instance=announce)
		if form.is_valid():
			form.save()
			if form.cleaned_data['send_email']:
				#generate+send email notification
				subject = 'New Announcement in '+c.department+' %s' %c.class_number
				from_email = 'itsatme@gmail.com'
				to = []
				for student in emailStudents:
					to.append(student.user.email)
				html_content = render_to_string('instructor/emailAnnounceTemplate.html', {'class': c, 'title': form.cleaned_data['title'], 'content': form.cleaned_data['content'], 'date_posted': datetime.datetime.now()})
				text_content = strip_tags(html_content)
				msg = EmailMultiAlternatives(subject, text_content, from_email, to)
				msg.attach_alternative(html_content, "text/html")
				msg.send()
			return HttpResponseRedirect("")
	else:
		form = AnnounceForm()
	
	content = getContent(c, user)
	content['form'] = form
	content['announcements'] = announcements
	return render_to_response('instructor/announcement.html', content, 
		context_instance=RequestContext(request))

#View to generate the page for the announcements view of Instructor App		
def updateAnnouncement(request, department, class_number, year, semester, section, anid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	an = get_object_or_404(Announcement, pk=anid)

	announcements = Announcement.objects.filter(cid=c.cid).order_by('-date_posted')
	
	if request.method == "POST":
		announce = Announcement(cid=c, date_posted=an.date_posted, uid=an.uid, was_updated=1, updated_by=user.userprofile, updated_on=datetime.datetime.now(), anid=anid)
		form = AnnounceForm(request.POST, instance=announce)
		if form.is_valid():
			form.save()
			url = getClassUrl(c) + 'instructor/announcement'
			return HttpResponseRedirect(url)
	else:
		tmp = Announcement.objects.get(anid=anid)
		form = AnnounceForm(initial={'title': tmp.title, 'content': tmp.content, 'send_email': tmp.send_email})
	
	content = getContent(c, user)
	content['form'] = form
	content['announcements'] = announcements
	return render_to_response('instructor/announcement.html', content, 
		context_instance=RequestContext(request))

#Remove announcement
def removeAnnouncement(request, department, class_number, year, semester, section, anid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	an = get_object_or_404(Announcement, pk=anid)

	# check if user has access
	accessToInst = instAccess(getInsts(c.cid), getTas(c.cid), user)

	if accessToInst:
		#delete announcement from database
		announcement = Announcement.objects.get(anid=anid)
		announcement.delete()
		url = getClassUrl(c) + 'instructor/announcement'
		return HttpResponseRedirect(url)
	else:
		content = {'accessToInst': accessToInst, 'classUrl': getClassUrl(c), }
		return render_to_response('instructor/announcement.html', content, 
			context_instance=RequestContext(request))
		
#Display class roster
def roster(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)	

	#Get all students in the class
	students = getStudents(c.cid)
	
	content = getContent(c, user)
	content['students'] = students
	return render_to_response('instructor/roster.html', content, 
		context_instance=RequestContext(request))

#Create and get grades for quizzes
def quizCreate(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)

	quizzes = Quiz.objects.filter(cid=c.cid)

	if request.method == 'POST':
		quiz = Quiz(cid=c)
		form = QuizForm(request.POST, instance=quiz)
		if form.is_valid():
			form.save()
			url = getClassUrl(c) + 'instructor/quiz/create/'
			return HttpResponseRedirect("")
	else:
		form = QuizForm()

	content = getContent(c, user)
	content['form'] = form
	content['quizzes'] = quizzes

	return render_to_response('instructor/quizCreate.html', content, 
		context_instance=RequestContext(request))

#Remove quizzes
def quizRemove(request, department, class_number, year, semester, section, qid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	q = get_object_or_404(Quiz, pk=qid)

	accessToInst = instAccess(getInsts(c.cid), getTas(c.cid), user)

	classUrl = getClassUrl(c)
	if accessToInst:
		#Delete quiz from database
		quiz = Quiz.objects.get(id=qid)
		quiz.delete()
		url = classUrl + 'instructor/quiz/create'
		return HttpResponseRedirect(url)
	else:
		content = {'accessToInst': accessToInst, 'classUrl': classUrl}
		return render_to_response('instructor/quizCreate.html', content, 
			context_instance=RequestContext(request))
			
def quizUpdate(request, department, class_number, year, semester, section, qid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	q = get_object_or_404(Quiz, pk=qid)
	
	quizzes = Quiz.objects.filter(cid=c.cid)

	if request.method == 'POST':
		form = QuizForm(request.POST)
		if form.is_valid():
			Quiz.objects.filter(id=q.id).update(name=form.cleaned_data["name"], start_date=form.cleaned_data["start_date"], end_date=form.cleaned_data["end_date"], student_attempts=form.cleaned_data["student_attempts"])
			url = getClassUrl(c) + 'instructor/quiz/create/'
			return HttpResponseRedirect(url)
	else:
		form = QuizForm(initial={'name': q.name, 'start_date': q.start_date, 'end_date': q.end_date, 'student_attempts': q.student_attempts} )

	content = getContent(c, user)
	content['form'] = form
	content['quizzes'] = quizzes

	return render_to_response('instructor/quizCreate.html', content, 
		context_instance=RequestContext(request))
					
def quizQuestions(request, department, class_number, year, semester, section, qid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	q = get_object_or_404(Quiz, pk=qid)
	
	#Create a formset of forms relating to the QuizQuestion model.
	QuizFormSet = modelformset_factory(QuizQuestion, can_delete=True, exclude=('qid'), extra=1)
	#Restrict quizzes displayed to only those for that quiz
	query = QuizQuestion.objects.filter(qid=qid)
	if request.method == "POST":
		formset = QuizFormSet(request.POST, queryset=query)
		if formset.is_valid():
			#Populate data for each form that isn't entered by the student
			for form in formset.forms:
				if form.has_changed():
					try: 
						QuizQuestion.objects.get(id=form.cleaned_data["id"].id)
						QuizQuestion.objects.filter(id=form.cleaned_data["id"].id).update(answer=form.cleaned_data["answer"], question=form.cleaned_data["question"], option1=form.cleaned_data["option1"], option2=form.cleaned_data["option2"], option3=form.cleaned_data["option3"], option4=form.cleaned_data["option4"])
					except:
						quiz = QuizQuestion(qid=q, answer=form.cleaned_data["answer"], question=form.cleaned_data["question"], option1=form.cleaned_data["option1"], option2=form.cleaned_data["option2"], option3=form.cleaned_data["option3"], option4=form.cleaned_data["option4"])
						form.instance = quiz
			formset.save()
			return HttpResponseRedirect("")
	else: 
		formset = QuizFormSet(queryset=query)
		
	content = getContent(c, user)
	content['formset'] = formset
	content['quiz'] = q
	return render_to_response('instructor/quizOptions.html', content,
		context_instance=RequestContext(request))

#Gets the grades for each student who has taken a certain quiz
def quizGrades(request, department, class_number, year, semester, section, qid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	q = get_object_or_404(Quiz, pk=qid)

	students = getStudents(c.cid)
	out_of = QuizQuestion.objects.filter(qid=qid).count()
	for student in students:
		#Gets all the quiz attempts for a certain quiz and a certain student
		gradesAgg = QuizAttempt.objects.filter(qid=qid, uid=student.id)
		#If the student has taken the quiz, return the best result
		if gradesAgg.count() > 0:
			student.grade = gradesAgg.aggregate(Max('result'))
		else: 
			student.grade = 0
	
	content = getContent(c, user)
	content["students"] = students
	content["quiz"] = q
	content["out_of"] = out_of
	return render_to_response('instructor/quizGrades.html', content, 
		context_instance=RequestContext(request))
				
# View for grades input
def grades(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	students = getStudents(c.cid)
	
	content = getContent(c, user)
	content['students'] = students
	return render_to_response('instructor/grades.html', content, 
		context_instance=RequestContext(request))

# View used for grades input via Excel files
def grades_files(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	students = getStudents(c.cid)
	
	message = ""
	error_message = ""
	
	# If statement to check if instructor/ta chose to upload or download grades file
	if request.method == 'POST':
		# If upload is chosen and form entry is valid, called upload_grades to upload
		# mark file for the associated activity
		if 'upload' in request.POST:
			form_upload = UploadGrade(request.POST, request.FILES, cid=c.cid)
			form_download = DownloadGrade(cid=c.cid)
			if form_upload.is_valid():
				# Verify file type (XLS only) and size (2MB max)
				uploaded_file = request.FILES['file_path']
				max_file_size = 2097152
				file_types_allowed = ['.xls',]
				isProperFileType = checkFileType(uploaded_file, file_types_allowed)
				isProperFileSize = checkFileSize(uploaded_file, max_file_size)
				if isProperFileType and isProperFileSize:	
					try:
						upload_grades(request.FILES['file_path'], request.POST['activity_name'])
						message = "Successfully uploaded grades"
					except:
						error_message = "Error: Format of Excel file is incorrect"
				elif not isProperFileType:
					error_message = "Error: File type is incorrect - must be .xls"
				elif not isProperFileSize:
					error_message = "Error: File size exceeds the max of 2MB"
		# If download is chosen and form entry is valid, called download_grades and serve
		# mark file of the associated activity to the instructor/ta
		elif 'download' in request.POST:
			form_download = DownloadGrade(request.POST, cid=c.cid)
			form_upload = UploadGrade(cid=c.cid)
			if form_download.is_valid():
				file_and_name = download_grades(students, request.POST['activity_name'])
				file_to_send = file_and_name['file']
				file_name = file_and_name['file_name']
				response = HttpResponse(file_to_send, content_type='application/vnd.ms-excel')
				response['Content-Disposition'] = 'attachment; filename='+file_name
				return response
	else:
		form_download = DownloadGrade(cid=c.cid)
		form_upload = UploadGrade(cid=c.cid)
	
	content = getContent(c, user)
	content['form_down'] = form_download
	content['form_up'] = form_upload
	content['error_message'] = error_message
	content['message'] = message
	content['students'] = students
	return render_to_response('instructor/fileGrades.html', content, 
		context_instance=RequestContext(request))

# Method used in grades_files view to upload grades
def upload_grades(input_file, aid):
	
	# Open/Read in the uploaded excel marks file
	excel_book = xlrd.open_workbook(file_contents=input_file.read())
	sheet = excel_book.sheet_by_index(0)
	num_of_rows = range(1,sheet.nrows)
	
	# Iterate through the marks file and input student marks for activity
	activity = Activity.objects.get(aid=aid)
	getcontext().prec = 2
	for row in num_of_rows:
		sfu_id = int(sheet.cell_value(row,3))
		user = UserProfile.objects.get(sfu_id=sfu_id)
		
		# Validating marks column for proper type
		mark_value = str(sheet.cell_value(row,4))
		if re.match("^[0-9.]+$", mark_value):
			if mark_value == '.':
				mark = Decimal(0)
			else:
				mark = Decimal(mark_value)
		else:
			mark = Decimal(0)
		
		# Check if user already has a grade recorded for the assignment:
		# - If they don't, then make a new Grade
		# - If they do, then update the grade to the new grade
		if Grade.objects.filter(uid=user.id, aid=aid).count() < 1:
			new_grade = Grade(uid=user, aid=activity)
			new_grade.mark = mark
			new_grade.save()
		else:
			update_grade = Grade.objects.get(uid=user.id, aid=aid)
			update_grade.mark = mark
			update_grade.save()

# Method used in grades_files view to download grades
def download_grades(student_list, aid):
	
	# Create a new excel marks file
	mark_file = xlwt.Workbook()
	sheet = mark_file.add_sheet('Marks')
	
	# Header row of marks file
	sheet.write(0,0, 'USERNAME')
	sheet.write(0,1, 'FIRST NAME')
	sheet.write(0,2, 'LAST NAME')
	sheet.write(0,3, 'SFU ID')
	sheet.write(0,4, 'MARK')
	
	# Populate the rows of the marks file with each student and their mark
	# for the associated activity
	activity = Activity.objects.get(aid=aid)
	file_name = activity.activity_name+".xls"
	row = 1
	for student in student_list:
		username = student.user.username
		first_name = student.user.first_name
		last_name = student.user.last_name
		sfu_id = student.sfu_id
		try:
			mark = Grade.objects.get(uid=student.user.id, aid=aid).mark
		except Grade.DoesNotExist:
			mark = None
		
		sheet.write(row,0, username)
		sheet.write(row,1, first_name)
		sheet.write(row,2, last_name)
		sheet.write(row,3, sfu_id)
		sheet.write(row,4, mark)
		row = row + 1
		
	#mark_file.save("/var/www/intrinsic-project/SOL/media/marks/"+file_name)
	#file_to_send = file("/var/www/intrinsic-project/SOL/media/marks/"+file_name)
	
	#mark_file.save("/Users/derek/Desktop/LOCAL/intrinsic-project/SOL/media/marks/"+file_name)
	#file_to_send = file("/Users/derek/Desktop/LOCAL/intrinsic-project/SOL/media/marks/"+file_name)
	
	mark_file.save("/Users/kevin/Dropbox/intrinsic-project Apr10/SOL/media/marks/"+file_name)
	file_to_send = file("/Users/kevin/Dropbox/intrinsic-project Apr10/SOL/media/marks/"+file_name)
	return { 'file': file_to_send, 'file_name': file_name }

# View for rendering the grade form for mark input
def grades_form(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	students = getStudents(c.cid)
	
	message = ""
	activity = ""
	existing_marks = {}
	
	form = OnlineGrade(cid=c.cid)
	if request.method == 'POST':
		if 'generate_form' in request.POST:
			form = OnlineGrade(request.POST, cid=c.cid)
			if form.is_valid():
				activity = Activity.objects.get(aid=request.POST['activity_name'])
				student_grades = Grade.objects.filter(aid=request.POST['activity_name'])
				
				for student in student_grades:
					existing_marks[int(student.uid.sfu_id)] = student.mark
	
	content = getContent(c, user)
	content['form'] = form
	content['message'] = message
	content['activity'] = activity
	content['existing_marks'] = existing_marks
	content['students'] = students
	return render_to_response('instructor/onlineGrades.html', content, 
		context_instance=RequestContext(request))

# View for inputting grades via an online form
def grades_input(request, department, class_number, year, semester, section, aid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	a = get_object_or_404(Activity, pk=aid)
	students = getStudents(c.cid)

	message = ""
	
	if request.method == 'POST':
		# Updates mark for each student in the class based on the inputted
		# value in the form
		if 'update' in request.POST:
			for student in students:
				# Validate mark input value
				mark_value = request.POST.__getitem__(str(student.sfu_id))
				if re.match("^[0-9.]+$", mark_value):
					if mark_value == '.':
						mark = Decimal(0)
					else:
						mark = Decimal(mark_value)
				else:
					mark = Decimal(0)
				
				uid = student.user.id
				
				# If the student already has a grade, update it
				# If the student does not have a grade, make a new one
				try:
					student_grade = Grade.objects.get(uid=uid, aid=aid)
				except Grade.DoesNotExist:
					student_grade = Grade(uid=student, aid=a)
				
				student_grade.mark = mark
				student_grade.save()
					
			message = "Successfully inputted student grades."
	
	content = getContent(c, user)
	content['message'] = message
	content['students'] = students
	return render_to_response('instructor/onlineGrades.html', content, 
		context_instance=RequestContext(request))

#Gets the generic contexts for all instructor views
def getContent(c, user):	
	instructors = getInsts(c.cid)
	tas = getTas(c.cid)
	latestAnnouncements = getAnnouncements(c.cid)
	for announce in latestAnnouncements:
		if (datetime.datetime.now() - announce.date_posted) < timedelta(days=1):
			announce.isNew = 1
		else:
			announce.isNew = 0

	content = {'class': c , 'instructors': instructors, 'tas': tas, 'accessToInst': instAccess(instructors, tas, user), 
		'class_list': getClassList(user), 'classUrl': getClassUrl(c), 'latestAnnouncements': latestAnnouncements}
	return content
