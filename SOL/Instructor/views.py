from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from Main.models import Course, ClassList
from Instructor.models import Announcement, Activity, CourseContent, Slide
from Gradebook.models import Grade, UploadGrade, DownloadGrade
from Student.views import instAccess, getInsts, getTas, getStudents, getClassUrl, getEnrolled, studentAccess, getAnnouncements, currentSemester
from forms import AnnounceForm, ActivityForm, CourseForm, GradeForm, SlideForm
from decimal import Decimal, getcontext
from reportlab.pdfgen import canvas
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
	#Get class if it exists, otherwise send a 404 page not found 
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	#get current user, all instructors and tas
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	#boolean field to see if user has access to instructor view
	accessToInst = instAccess(instructors, tas, user)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
	#render to specified template sending specified variables
	content = {'class': c, 'classUrl': getClassUrl(c), 'accessToInst': accessToInst, 'class_list': class_list}	
	return render_to_response('instructor/index.html', content,
		context_instance=RequestContext(request))

#View to generate the page for the syllabus view of Instructor App
def syllabus(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	classUrl = getClassUrl(c)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
	if request.method == 'POST':
		content = CourseContent(cid=c, created_on=datetime.datetime.now(), was_updated=0, updated_on=datetime.datetime.now() )
		form = CourseForm(request.POST, instance=content)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		try:
			course = CourseContent.objects.get(cid=class_id)
			return HttpResponseRedirect(classUrl+"instructor/syllabus/update/%s" %course.id)
		except CourseContent.DoesNotExist:
			form = CourseForm()
	
	content = {'class': c, 'accessToInst': accessToInst, 'form': form, 'classUrl': classUrl, 'class_list': class_list }
	return render_to_response('instructor/syllabus.html', content, 
		context_instance=RequestContext(request))

#View to update the graded activity in the Instructor App
def updateSyllabus(request, department, class_number, year, semester, section, sid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	s = get_object_or_404(CourseContent, pk=sid)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	classUrl = getClassUrl(c)

	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)

	message = ''
	if request.method == 'POST':
		course = CourseContent(id=sid, cid=c, created_on=s.created_on, was_updated=1, updated_on=datetime.datetime.now() )
		form = CourseForm(request.POST, instance=course)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(classUrl+"instructor/syllabus/")
	else:
		course = CourseContent.objects.get(cid=class_id)
		form = CourseForm(initial={'officeHrs': course.officeHrs, 'officeLocation': course.officeLocation, 'phoneNumber': course.phoneNumber, 'TaOfficeLocation': course.TaOfficeLocation, 'TaOfficeHrs': course.TaOfficeHrs, 'lectTime': course.lectTime, 'prereq': course.prereq, 'books': course.books, 'topics': course.topics, 'markingScheme': course.markingScheme, 'academicHonesty': course.academicHonesty, 'additionalInfo': course.additionalInfo, 'file_path': course.file_path,})
	
	content = {'class': c, 'accessToInst': accessToInst, 'form': form, 'classUrl': classUrl, 'class_list': class_list}
	return render_to_response('instructor/syllabus.html', content, 
		context_instance=RequestContext(request))

def slides(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	enrolled = getEnrolled(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	
	slides = Slide.objects.filter(cid=class_id)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
	if request.method == 'POST':
		slide = Slide(cid=c, uploaded_on=datetime.datetime.now())
		form = SlideForm(request.POST, request.FILES, instance=slide)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		form = SlideForm()
	content = {'class': c, 'accessToInst': accessToInst, 'form': form, 'classUrl': getClassUrl(c), 'slides':slides,
	'class_list': class_list }
	return render_to_response('instructor/slides.html', content, 
		context_instance=RequestContext(request))
		
def updateSlides(request, department, class_number, year, semester, section, slid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	s = get_object_or_404(Slide, pk=slid)

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	enrolled = getEnrolled(class_id)

	accessToInst = instAccess(instructors, tas, user)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
	slides = Slide.objects.filter(cid=class_id)
	
	if request.method == 'POST':
		slide = Slide(cid=c, uploaded_on=datetime.datetime.now(), id=slid)
		form = SlideForm(request.POST, request.FILES, instance=slide)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		form = SlideForm(initial={'title': s.title, 'file_path': s.file_path})
	content = {'class': c, 'accessToInst': accessToInst, 'form': form, 'classUrl': getClassUrl(c), 'slides': slides,
	'class_list': class_list }
	return render_to_response('instructor/slides.html', content, 
		context_instance=RequestContext(request))
		
def removeSlides(request, department, class_number, year, semester, section, slid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	s = get_object_or_404(Slide, pk=slid)

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)

	accessToInst = instAccess(instructors, tas, user)

	if accessToInst:
		slide = Slide.objects.get(id=slid)
		slide.delete()
		url ='/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/instructor/slides'
		return HttpResponseRedirect(url)
	else:
		content = {'accessToInst': accessToInst, 'classUrl': getClassUrl(c)}
		return render_to_response('instructor/slides.html', content, 
			context_instance=RequestContext(request))
			
#View to generate the page for the graded activities view of Instructor App
def activity(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	enrolled = getEnrolled(class_id)
	emailStudents = UserProfile.objects.filter(classlist__cid=class_id, setting__email_activity=1)
	
	accessToInst = instAccess(instructors, tas, user)
	activities = Activity.objects.filter(cid=class_id)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
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
	content = {'class': c, 'accessToInst': accessToInst, 'form': form, 'activities': activities, 'update':0, 'classUrl': getClassUrl(c),
	'class_list': class_list }
	return render_to_response('instructor/activity.html', content, 
		context_instance=RequestContext(request))
		
#View to update the graded activity in the Instructor App
def updateActivity(request, department, class_number, year, semester, section, aid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	a = get_object_or_404(Activity, pk=aid)

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	enrolled = getEnrolled(class_id)
	emailStudents = UserProfile.objects.filter(classlist__cid=class_id, setting__email_activity=1)

	accessToInst = instAccess(instructors, tas, user)
	activities = Activity.objects.filter(cid=class_id)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)

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
			url ='/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/instructor/activity'
			return HttpResponseRedirect(url)
	else:
		tmp = Activity.objects.get(aid=aid)
		form = ActivityForm(initial={'activity_name': tmp.activity_name, 'out_of': tmp.out_of, 'worth': tmp.worth, 'description': tmp.description, 'description_doc': tmp.description_doc, 'due_date': tmp.due_date, 'status': tmp.status, })

	content = {'class': c, 'accessToInst': accessToInst, 'form': form, 'activities': activities, 'update':1, 'classUrl': getClassUrl(c),
	'class_list': class_list }
	return render_to_response('instructor/activity.html', content, 
		context_instance=RequestContext(request))
		
#View to delete the graded activity in the Instructor App
def removeActivity(request, department, class_number, year, semester, section, aid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	a = get_object_or_404(Activity, pk=aid)

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)

	accessToInst = instAccess(instructors, tas, user)

	if accessToInst:
		activity = Activity.objects.get(aid=aid)
		activity.delete()
		url ='/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/instructor/activity'
		return HttpResponseRedirect(url)
	else:
		content = {'accessToInst': accessToInst, 'classUrl': getClassUrl(c)}
		return render_to_response('instructor/announcement.html', content, 
			context_instance=RequestContext(request))

#View to generate the page for the announcements view of Instructor App	
def announcement(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	enrolled = getEnrolled(class_id)
	emailStudents = UserProfile.objects.filter(classlist__cid=class_id, setting__email_announcement=1)
	
	accessToInst = instAccess(instructors, tas, user)
	announcements = Announcement.objects.filter(cid=class_id).order_by('-date_posted')
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
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
	
	content = {'class': c, 'form': form, 'accessToInst': accessToInst, 'announcements': announcements, 'classUrl': getClassUrl(c),
	'class_list': class_list }
	return render_to_response('instructor/announcement.html', content, 
		context_instance=RequestContext(request))

#View to generate the page for the announcements view of Instructor App		
def updateAnnouncement(request, department, class_number, year, semester, section, anid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	an = get_object_or_404(Announcement, pk=anid)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	announcements = Announcement.objects.filter(cid=class_id).order_by('-date_posted')

	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
	if request.method == "POST":
		announce = Announcement(cid=c, date_posted=an.date_posted, uid=an.uid, was_updated=1, updated_by=user.userprofile, updated_on=datetime.datetime.now(), anid=anid)
		form = AnnounceForm(request.POST, instance=announce)
		if form.is_valid():
			form.save()
			url ='/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/instructor/announcement'
			return HttpResponseRedirect(url)
	else:
		tmp = Announcement.objects.get(anid=anid)
		form = AnnounceForm(initial={'title': tmp.title, 'content': tmp.content, 'send_email': tmp.send_email})
	
	content = {'class': c, 'form': form, 'announcements': announcements, 'accessToInst': accessToInst, 'classUrl': getClassUrl(c),
	'class_list': class_list }
	return render_to_response('instructor/announcement.html', content, 
		context_instance=RequestContext(request))

def removeAnnouncement(request, department, class_number, year, semester, section, anid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	an = get_object_or_404(Announcement, pk=anid)

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)

	accessToInst = instAccess(instructors, tas, user)

	if accessToInst:
		announcement = Announcement.objects.get(anid=anid)
		announcement.delete()
		url ='/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/instructor/announcement'
		return HttpResponseRedirect(url)
	else:
		content = {'accessToInst': accessToInst, 'classUrl': getClassUrl(c), }
		return render_to_response('instructor/announcement.html', content, 
			context_instance=RequestContext(request))

def addGrades(request, department, class_number, year, semester, section, aid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	a = get_object_or_404(Activity, pk=aid)

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)

	accessToInst = instAccess(instructors, tas, user)
	students = getStudents(class_id)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	
	if request.method == 'POST':
		#form = UploadGrade(request.POST, request.FILES)
		grade = Grade(aid=aid)
		form = GradeForm(request.Post, instance=grade)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		theForm = GradeForm()
		GradeFormSet = modelformset_factory(GradeForm)
		formset = GradeFormSet()

	content = {'class': c, 'formset': formset, 'accessToInst': accessToInst, 'students': students, 'classUrl': getClassUrl(c), 'class_list': class_list}
	return render_to_response('instructor/grades.html', content, 
		context_instance=RequestContext(request))
		
def roster(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)		

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)

	accessToInst = instAccess(instructors, tas, user)
	students = getStudents(class_id)
	
	content = {'class': c, 'accessToInst': accessToInst, 'instructors': instructors, 'tas':tas, 'students': students, 
	'classUrl': getClassUrl(c), 'class_list': class_list}
	return render_to_response('instructor/roster.html', content, 
		context_instance=RequestContext(request))

def formTable(form, students):
	foo = []
	i = 0;
	for student in students:
		foo.insert(i, GradeForm(initial={'uid':student.user.id, }))
		i += 1
	return foo

def grades(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)

	accessToInst = instAccess(instructors, tas, user)
	students = getStudents(class_id)
	
	year = datetime.date.today().year
	semester = currentSemester()
	class_list = Course.objects.filter(classlist__uid=user.id, year=year, semester=semester)
	message = ""
	
	if request.method == 'POST':
		if 'upload' in request.POST:
			form_upload = UploadGrade(request.POST, request.FILES, cid=class_id)
			form_download = DownloadGrade(cid=class_id)
			if form_upload.is_valid():
				upload_grades(request.FILES['file_path'], request.POST['activity_name'])
				message = "Successfully uploaded grades."
		elif 'download' in request.POST:
			form_download = DownloadGrade(request.POST, cid=class_id)
			form_upload = UploadGrade(cid=class_id)
			if form_download.is_valid():
				file_and_name = download_grades(class_id, request.POST['activity_name'])
				file_to_send = file_and_name['file']
				file_name = file_and_name['file_name']
				response = HttpResponse(file_to_send, content_type='application/vnd.ms-excel')
				response['Content-Disposition'] = 'attachment; filename='+file_name
				return response
	else:
		#options = Activity.objects.filter(cid=class_id)
		form_upload = UploadGrade(cid=class_id)
		form_download = DownloadGrade(cid=class_id)
	
	content = {'class': c, 'classUrl': getClassUrl(c), 'form_up': form_upload, 'form_down': form_download, 'message': message,
	'accessToInst': accessToInst, 'students': students, 'class_list': class_list}
	return render_to_response('instructor/grades.html', content, 
		context_instance=RequestContext(request))

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

def download_grades(cid, aid):
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
	class_list = ClassList.objects.filter(cid=cid)
	row = 1
	for person in class_list:
		if not person.is_instructor and not person.is_ta:
			username = person.uid.user.username
			first_name = person.uid.user.first_name
			last_name = person.uid.user.last_name
			sfu_id = person.uid.sfu_id
			try:
				mark = Grade.objects.get(uid=person.uid.user.id, aid=aid).mark
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
#def getRequiredContent(department, class_number, year, semester, section):
	
