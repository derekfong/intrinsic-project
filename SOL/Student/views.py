from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from Main.models import Course, ClassList, UserProfile
from django.contrib.auth.models import User
from Instructor.models import Activity

# Create your views here.
def index(request, department, class_number, year, semester, section):

	# student has to find corresponding COURSE model
	# Course has general info about dept, faculty, class number, semester, etc it belongs to
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user
	
	instructors = getInsts(class_id)
	tas = getTas(class_id)
	students = getStudents(class_id)

	accessToInst = instAccess(instructors, tas, user)
	accessToStudent = studentAccess(students, user)
	
	return render_to_response('student/index.html', {'class': c , 'instructors': instructors, 'tas': tas, 'students': students, 'accessToInst': accessToInst, 'accessToStudent': accessToStudent,},
		context_instance=RequestContext(request))


# activities is an assignment, midterm, etc
def activities(request, department, class_number, year, semester, section):
	# get corresponding dept, class num, year, etc
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester, section=section).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user

	students = getStudents(class_id)

	# make sure it is the right activity for that associated class	
	activities = Activity.objects.filter(cid=class_id)

	accessToStudent = studentAccess(students, user)
	return render_to_response('student/activities.html', {'accessToStudent': accessToStudent, 'class': c, 'activities': activities, }, context_instance=RequestContext(request))
			

## these check for permission (whether allowed access as student or as T.A.)
## permissions allow different features		
def instAccess(instructors, tas, user):
	for ta in tas:
		for instructor in instructors:
			if user.id in [ta.user.id, instructor.user.id]:
				return 1
	return 0

def studentAccess(students, user):
	for student in students:
		if user.id == student.user.id:
			return 1
	return 0

## SETTERS AND GETTERS
## for TAs / Ints / students 
def getInsts(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id, classlist__is_instructor=1)

def getTas(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id, classlist__is_ta=1)

def getStudents(class_id):
	return UserProfile.objects.filter(classlist__cid=class_id, classlist__is_ta=0, classlist__is_instructor=0)
