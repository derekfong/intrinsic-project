from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from Main.models import Course, ClassList

# Create your views here.
def index(request, department, class_number, year, semester):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user
	instruct_access = ClassList.objects.filter(cid=class_id, uid=user.id, is_instructor=True).count()
	ta_access= ClassList.objects.filter(cid=class_id, uid=user.id, is_ta=True).count()
	return render_to_response('instructor/index.html', {'class': c, 'instruct_access': instruct_access, 'ta_access': ta_access },
		context_instance=RequestContext(request))

def syllabus(request, department, class_number, year, semester):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user
	instruct_access = ClassList.objects.filter(cid=class_id, uid=user.id, is_instructor=True).count()
	ta_access= ClassList.objects.filter(cid=class_id, uid=user.id, is_ta=True).count()
	return render_to_response('instructor/syllabus.html', {'class': c, 'instruct_access': instruct_access, 'ta_access': ta_access}, 
		context_instance=RequestContext(request))
		
def activity(request, department, class_number, year, semester):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user
	instruct_access = ClassList.objects.filter(cid=class_id, uid=user.id, is_instructor=True).count()
	ta_access= ClassList.objects.filter(cid=class_id, uid=user.id, is_ta=True).count()
	return render_to_response('instructor/activity.html', {'class': c, 'instruct_access': instruct_access, 'ta_access': ta_access}, 
		context_instance=RequestContext(request))
		
def announcement(request, department, class_number, year, semester):
	class_id = Course.objects.get(department=department, class_number=class_number, year=year, semester=semester).cid
	c = get_object_or_404(Course, pk=class_id)
	user = request.user
	instruct_access = ClassList.objects.filter(cid=class_id, uid=user.id, is_instructor=True).count()
	ta_access= ClassList.objects.filter(cid=class_id, uid=user.id, is_ta=True).count()
	return render_to_response('instructor/announcement.html', {'class': c, 'instruct_access': instruct_access, 'ta_access': ta_access}, 
		context_instance=RequestContext(request))