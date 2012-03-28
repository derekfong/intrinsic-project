from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from Main.models import Course, ClassList
from Instructor.models import Announcement, Activity, CourseContent, Slide
from Gradebook.models import Grade, UploadGrade, DownloadGrade, OnlineGrade
from Student.views import instAccess, getInsts, getTas, getStudents, getClassUrl, getEnrolled, studentAccess, getAnnouncements, currentSemester, getClassObject, getClassList
from forms import AnnounceForm, ActivityForm, CourseForm, GradeForm, SlideForm
from decimal import Decimal, getcontext
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from Main.models import UserProfile
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import datetime, xlrd, xlwt, re

#View to generate the page for the main view of Instructor App
def index(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	content = getContent(c, user)
	return render_to_response('instructor/index.html', content,
		context_instance=RequestContext(request))

#View to generate the page for the syllabus view of Instructor App
def syllabus(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	
	message = ''
	classUrl = getClassUrl(c)
	if request.method == 'POST':
		content = CourseContent(cid=c, created_on=datetime.datetime.now(), was_updated=0, updated_on=datetime.datetime.now() )
		form = CourseForm(request.POST, instance=content)
		if form.is_valid():
			form.save()
			message = 'You have successfully created a syllabus'
	else:
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

#View to update the graded activity in the Instructor App
def updateSyllabus(request, department, class_number, year, semester, section, sid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	s = get_object_or_404(CourseContent, pk=sid)
	
	message = ''
	classUrl = getClassUrl(c)
	if request.method == 'POST':
		course = CourseContent(id=sid, cid=c, created_on=s.created_on, was_updated=1, updated_on=datetime.datetime.now() )
		form = CourseForm(request.POST, instance=course)
		if form.is_valid():
			form.save()
			message = 'You have successfully updated the syllabus'
	else:
		course = CourseContent.objects.get(cid=c.cid)
		form = CourseForm(initial={'officeHrs': course.officeHrs, 'officeLocation': course.officeLocation, 'phoneNumber': course.phoneNumber, 'TaOfficeLocation': course.TaOfficeLocation, 'TaOfficeHrs': course.TaOfficeHrs, 'lectTime': course.lectTime, 'prereq': course.prereq, 'books': course.books, 'topics': course.topics, 'markingScheme': course.markingScheme, 'academicHonesty': course.academicHonesty, 'additionalInfo': course.additionalInfo, 'file_path': course.file_path,})
	
	content = getContent(c, user)
	content['form'] = form
	content['classUrl'] = classUrl
	content['message'] = message
	return render_to_response('instructor/syllabus.html', content, 
		context_instance=RequestContext(request))

def slides(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
		
	slides = Slide.objects.filter(cid=c.cid)
	
	if request.method == 'POST':
		slide = Slide(cid=c, uploaded_on=datetime.datetime.now())
		form = SlideForm(request.POST, request.FILES, instance=slide)
		if form.is_valid():
			form.save()
			HttpResponseRedirect("")
	else:
		form = SlideForm()
		
	content = getContent(c, user)
	content['form'] = form
	content['slides'] = slides

	return render_to_response('instructor/slides.html', content, 
		context_instance=RequestContext(request))
		
def updateSlides(request, department, class_number, year, semester, section, slid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	s = get_object_or_404(Slide, pk=slid)

	slides = Slide.objects.filter(cid=c.cid)
	
	classUrl = getClassUrl(c)
	if request.method == 'POST':
		slide = Slide(cid=c, uploaded_on=datetime.datetime.now(), id=slid)
		form = SlideForm(request.POST, request.FILES, instance=slide)
		if form.is_valid():
			form.save()
			url = classUrl +'instructor/slides'
			return HttpResponseRedirect(url)
	else:
		form = SlideForm(initial={'title': s.title, 'file_path': s.file_path})
	
	content = getContent(c, user)
	content['form'] = form
	content['slides'] = slides
	return render_to_response('instructor/slides.html', content, 
		context_instance=RequestContext(request))
		
def removeSlides(request, department, class_number, year, semester, section, slid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
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
		
	emailStudents = UserProfile.objects.filter(classlist__cid=c.cid, setting__email_activity=1)
	activities = Activity.objects.filter(cid=c.cid)
	
	if request.method == 'POST':
		activity = Activity(cid=c)
		form = ActivityForm(request.POST, request.FILES, instance=activity)
		if form.is_valid():
			form.save()
			if form.cleaned_data['status'] == 2:
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

	emailStudents = UserProfile.objects.filter(classlist__cid=c.cid, setting__email_activity=1)
	activities = Activity.objects.filter(cid=c.cid)
	
	if request.method == 'POST':
		activity = Activity(cid=c, aid=aid)
		form = ActivityForm(request.POST, request.FILES, instance=activity)
		if form.is_valid():
			form.save()
			if form.cleaned_data['status'] == 2:
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
			url = getClassUrl(c) + 'instructor/activity'
			return HttpResponseRedirect(url)
	else:
		tmp = Activity.objects.get(aid=aid)
		form = ActivityForm(initial={'activity_name': tmp.activity_name, 'out_of': tmp.out_of, 'worth': tmp.worth, 'description': tmp.description, 'description_doc': tmp.description_doc, 'due_date': tmp.due_date, 'status': tmp.status, })

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
		activity = Activity.objects.get(aid=aid)
		activity.delete()
		url = getClassUrl(c) + 'instructor/activity'
		return HttpResponseRedirect(url)
	else:
		content = {'accessToInst': accessToInst, 'classUrl': getClassUrl(c)}
		return render_to_response('instructor/announcement.html', content, 
			context_instance=RequestContext(request))

#View to generate the page for the announcements view of Instructor App	
def announcement(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)

	emailStudents = UserProfile.objects.filter(classlist__cid=c.cid, setting__email_announcement=1)
	announcements = Announcement.objects.filter(cid=c.cid).order_by('-date_posted')

	if request.method == 'POST':
		announce = Announcement(cid=c, uid=user.userprofile, was_updated=0, updated_on=datetime.datetime.now(), updated_by=user.userprofile, date_posted=datetime.datetime.now())
		form = AnnounceForm(request.POST, instance=announce)
		if form.is_valid():
			form.save()
			if form.cleaned_data['send_email']:
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

def removeAnnouncement(request, department, class_number, year, semester, section, anid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	an = get_object_or_404(Announcement, pk=anid)

	accessToInst = instAccess(getInsts(c.cid), getTas(c.cid), user)

	if accessToInst:
		announcement = Announcement.objects.get(anid=anid)
		announcement.delete()
		url = getClassUrl(c) + 'instructor/announcement'
		return HttpResponseRedirect(url)
	else:
		content = {'accessToInst': accessToInst, 'classUrl': getClassUrl(c), }
		return render_to_response('instructor/announcement.html', content, 
			context_instance=RequestContext(request))
		
def roster(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)	

	students = getStudents(c.cid)
	
	content = getContent(c, user)
	content['students'] = students
	return render_to_response('instructor/roster.html', content, 
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
	if request.method == 'POST':
		if 'upload' in request.POST:
			form_upload = UploadGrade(request.POST, request.FILES, cid=c.cid)
			form_download = DownloadGrade(cid=c.cid)
			if form_upload.is_valid():
				upload_grades(request.FILES['file_path'], request.POST['activity_name'])
				message = "Successfully uploaded grades."
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
	content['form_upload'] = form_upload
	content['message'] = message
	content['students'] = students
	return render_to_response('instructor/fileGrades.html', content, 
		context_instance=RequestContext(request))

# Method used in grades_files view to upload grades
def upload_grades(input_file, aid):
	excel_book = xlrd.open_workbook(file_contents=input_file.read())
	sheet = excel_book.sheet_by_index(0)
	num_of_rows = range(1,sheet.nrows)
	
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
	mark_file = xlwt.Workbook()
	sheet = mark_file.add_sheet('Marks')
	
	# Header row
	sheet.write(0,0, 'USERNAME')
	sheet.write(0,1, 'FIRST NAME')
	sheet.write(0,2, 'LAST NAME')
	sheet.write(0,3, 'SFU ID')
	sheet.write(0,4, 'MARK')
	
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
	mark_file.save("/var/www/intrinsic-project/SOL/media/marks/"+file_name)
	file_to_send = file("/var/www/intrinsic-project/SOL/media/marks/"+file_name)
	return { 'file': file_to_send, 'file_name': file_name }

# View for rendering the grade form for mark input
def grades_form(request, department, class_number, year, semester, section):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	students = getStudents(c.cid)
	
	message = ""
	activity = ""
	form = OnlineGrade(cid=c.cid)
	if request.method == 'POST':
		if 'generate_form' in request.POST:
			form = OnlineGrade(request.POST, cid=c.cid)
			if form.is_valid():
				activity = Activity.objects.get(aid=request.POST['activity_name'])
	content = getContent(c, user)
	content['form'] = form
	content['message'] = message
	content['activity'] = activity
	content['students'] = students
	return render_to_response('instructor/onlineGrades.html', content, 
		context_instance=RequestContext(request))

# View for inputting grades via an online form
def grades_input(request, department, class_number, year, semester, section, aid):
	user = request.user
	c = getClassObject(department, class_number, year, semester, section, user)
	students = getStudents(c.cid)

	# ADD INITALLY POPULATED MARKS
	message = ""
	if request.method == 'POST':
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
				
				try:
					student_grade = Grade.objects.get(uid=uid, aid=aid)
				except Grade.DoesNotExist:
					student_grade = Grade(uid=student, aid=Activity.objects.get(aid=aid))
				
				
				student_grade.mark = mark
				student_grade.save()
			message = "Successfully inputted student grades."
	
	content = getContent(c, user)
	content['message'] = message
	content['students'] = students
	return render_to_response('instructor/onlineGrades.html', content, 
		context_instance=RequestContext(request))

def getContent(c, user):
	instructors = getInsts(c.cid)
	tas = getTas(c.cid)

	content = {'class': c , 'instructors': instructors, 'tas': tas, 'accessToInst': instAccess(instructors, tas, user), 
		'class_list': getClassList(user), 'classUrl': getClassUrl(c), }
	return content