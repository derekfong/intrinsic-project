from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from Main.models import Course, ClassList
from Instructor.models import Announcement, Activity, CourseContent
from Gradebook.models import Grade, UploadGrade
from Student.views import instAccess, getInsts, getTas, getStudents, getClassUrl
from forms import AnnounceForm, ActivityForm, CourseForm, GradeForm
from decimal import Decimal, getcontext
import datetime, xlrd, xlwt
from reportlab.pdfgen import canvas
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User
from Main.models import UserProfile

# Create your views here.
def index(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	
	content = {'class': c, 'classUrl': getClassUrl(c), 'accessToInst': accessToInst, }	
	return render_to_response('instructor/index.html', content,
		context_instance=RequestContext(request))

def syllabus(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	
	
	if request.method == 'POST':
		content = CourseContent(cid=class_id)
		form = CourseForm(request.POST, instance=content)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		count = CourseContent.objects.filter(cid=class_id).count()
		if count == 1:
			course = CourseContent.objects.get(cid=class_id)
			form = CourseForm(initial={'officeHrs': course.officeHrs, 'officeLocation': course.officeLocation, 'phoneNumber': course.phoneNumber, 'TaOfficeLocation': course.TaOfficeLocation, 'TaOfficeHrs': course.TaOfficeHrs, 'lectTime': course.lectTime, 'prereq': course.prereq, 'books': course.books, 'topics': course.topics, 'markingScheme': course.markingScheme, 'academicHonesty': course.academicHonesty, 'additionalInfo': course.additionalInfo, 'file_path': course.file_path,})
		else:
			form = CourseForm()
	
	content = {'class': c, 'accessToInst': accessToInst, 'form': form, 'classUrl': getClassUrl(c), }
	return render_to_response('instructor/syllabus.html', content, 
		context_instance=RequestContext(request))
			
		
def activity(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	activities = Activity.objects.filter(cid=class_id)
	
	if request.method == 'POST':
		activity = Activity(cid=c)
		form = ActivityForm(request.POST, instance=activity)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		form = ActivityForm()
	
	content = {'class': c, 'accessToInst': accessToInst, 'form': form, 'activities': activities, 'update':0, 'classUrl': getClassUrl(c), }
	return render_to_response('instructor/activity.html', content, 
		context_instance=RequestContext(request))
		
def updateActivity(request, department, class_number, year, semester, section, aid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	a = get_object_or_404(Activity, pk=aid)

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)

	accessToInst = instAccess(instructors, tas, user)
	activities = Activity.objects.filter(cid=class_id)

	if request.method == 'POST':
		activity = Activity(cid=c, aid=aid)
		form = ActivityForm(request.POST, instance=activity)
		if form.is_valid():
			form.save()
			url ='/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/instructor/activity'
			return HttpResponseRedirect(url)
	else:
		tmp = Activity.objects.get(aid=aid)
		form = ActivityForm(initial={'activity_name': tmp.activity_name, 'out_of': tmp.out_of, 'worth': tmp.worth, 'due_date': tmp.due_date, 'status': tmp.status, })

	content = {'class': c, 'accessToInst': accessToInst, 'form': form, 'activities': activities, 'update':1, 'classUrl': getClassUrl(c), }
	return render_to_response('instructor/activity.html', content, 
		context_instance=RequestContext(request))
		
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
		
def announcement(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	announcements = Announcement.objects.filter(cid=class_id).order_by('-date_posted')
	
	if request.method == 'POST':
		announce = Announcement(cid=c, uid=user.userprofile, was_updated=0, updated_on=datetime.datetime.now(), updated_by=user.userprofile, date_posted=datetime.datetime.now())
		form = AnnounceForm(request.POST, instance=announce)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("")
	else:
		form = AnnounceForm()
	
	content = {'class': c, 'form': form, 'accessToInst': accessToInst, 'announcements': announcements, 'classUrl': getClassUrl(c) }
	return render_to_response('instructor/announcement.html', content, 
		context_instance=RequestContext(request))
		
def updateAnnouncement(request, department, class_number, year, semester, section, anid):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	an = get_object_or_404(Announcement, pk=anid)
	
	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	
	accessToInst = instAccess(instructors, tas, user)
	announcements = Announcement.objects.filter(cid=class_id).order_by('-date_posted')
	
	if request.method == "POST":
		announce = Announcement(cid=c, date_posted=an.date_posted, uid=an.uid, was_updated=1, updated_by=user.userprofile, updated_on=datetime.datetime.now(), anid=anid)
		form = AnnounceForm(request.POST, instance=announce)
		if form.is_valid():
			form.save()
			url ='/course/'+c.department+'/%s' %c.class_number+'/%s' %c.year+'/'+c.semester+'/'+c.section+'/instructor/announcement'
			return HttpResponseRedirect(url)
	else:
		tmp = Announcement.objects.get(anid=anid)
		form = AnnounceForm(initial={'title': tmp.title, 'content': tmp.content })
	
	content = {'class': c, 'form': form, 'announcements': announcements, 'accessToInst': accessToInst, 'classUrl': getClassUrl(c) }
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

	content = {'class': c, 'formset': formset, 'accessToInst': accessToInst, 'students': students, 'classUrl': getClassUrl(c)}
	return render_to_response('instructor/grades.html', content, 
		context_instance=RequestContext(request))
		
def roster(request, department, class_number, year, semester, section):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)		

	user = request.user
	instructors = getInsts(class_id)
	tas = getTas(class_id)

	accessToInst = instAccess(instructors, tas, user)
	students = getStudents(class_id)
	
	content = {'class': c, 'accessToInst': accessToInst, 'instructors': instructors, 'tas':tas, 'students': students, 'classUrl': getClassUrl(c)}
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
	
	message = ""
	
	if request.method == 'POST':
		form = UploadGrade(request.POST, request.FILES, cid=class_id)
		if form.is_valid():
			upload_grades(request.FILES['file_path'], request.POST['activity_name'])
			message = "Successfully uploaded grades."
	else:
		options = Activity.objects.filter(cid=class_id)
		form = UploadGrade(cid=class_id)
		
	content = {'class': c, 'form': form, 'message': message, 'accessToInst': accessToInst, 'students': students}
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
		mark = Decimal(sheet.cell_value(row,4))
		user = UserProfile.objects.get(sfu_id=sfu_id)
		new_grade = Grade(uid=user, aid=activity)
		new_grade.mark = mark
		new_grade.save()


#def getRequiredContent(department, class_number, year, semester, section):
	
