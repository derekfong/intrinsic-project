# Create your views here.
from Forum.models import *
from Main.models import Course
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from SOL.Student.views import *



# choose which topic to view
def topic_display(request, department, class_number, year, semester, section):

	user = request.user
	current_course = getClassObject(department, class_number, year, semester, section, user)

	# list all topics of a course
	topics = Topics.objects.filter(course = current_course.cid, not_deleted=True)
	classUrl = getClassUrl(current_course)
	
	# see if instructor or current user which means they are allowed to remove their posts
	instructors = getInsts(current_course.cid)
	tas = getTas(current_course.cid)	

	if request.method == 'POST':
		if len(str(request.POST['title'])) <=1 or len(str(request.POST['message'])) <=1:
			error_message = "Please make sure all fields are filled."


			content = getContent(current_course, user)
			content['error_message'] = error_message
			content['topics'] = topics
			content['classUrl'] = classUrl
			content['instAccess'] = instAccess(instructors, tas, user)

			return render_to_response("forum/topic_display.html", content, context_instance=RequestContext(request))

		else: 

			user_topic = Topics(topic_name = request.POST['title'], course = current_course)
			user_topic.save()

			new_topic = Topics.objects.get(topic_name = request.POST['title'], course=current_course, id=user_topic.id)

			# use new topic id that was just created
			user_post = Messages(topic = new_topic, user = request.user, message = request.POST['message'])
			user_post.save()

			return HttpResponseRedirect(classUrl+"forum/")

	content = getContent(current_course, user)
	content['topics'] = topics
	content['classUrl'] = classUrl
	content['instAccess'] = instAccess(instructors, tas, user)

	return render_to_response("forum/topic_display.html", content, context_instance=RequestContext(request))


# list out all messages for that course
def message_display(request, department, class_number, year, semester, section, topic_id):
# no more course_id or topic_id 

	# get all the msgs relating to the specific topic_id
	msgs = Messages.objects.filter(topic = topic_id)

	user = request.user
	current_course = getClassObject(department, class_number, year, semester, section, user)

	# this is for inserting post into database (see below)
	# use course_id and topic_id as a superkey
	current_topic = Topics.objects.get(course = current_course, id = topic_id)

	classUrl = getClassUrl(current_course)

	# see if instructor or current user which means they are allowed to remove their posts
	instructors = getInsts(current_course.cid)
	tas = getTas(current_course.cid)	


	if request.method == 'POST':
		if len(str(request.POST['message'])) <=1:
			error_message = "Please fill out the message box before hitting Submit."

			content = getContent(current_course, user)
			content['messages'] = msgs
			content['classUrl'] = classUrl
			content['error_message'] = error_message
			content['topic'] = current_topic
			content['instAccess'] = instAccess(instructors, tas, user)

			return render_to_response("forum/message_display.html", content, context_instance=RequestContext(request))

		else: 
			user_post = Messages(topic = current_topic, user = request.user, message = request.POST['message'])
			user_post.save()
			return HttpResponseRedirect(classUrl+"forum/" + topic_id)

	instructors = getInsts(current_course.cid)
	tas = getTas(current_course.cid)	

	content = getContent(current_course, user)
	content['messages'] = msgs
	content['classUrl'] = classUrl
	content['topic'] = current_topic
	content['instAccess'] = instAccess(instructors, tas, user)

	return render_to_response("forum/message_display.html", content, context_instance=RequestContext(request))


def remove_topic(request, department, class_number, year, semester, section, topic_id):
	user = request.user


	current_course = getClassObject(department, class_number, year, semester, section, user)
	current_topic = Topics.objects.get(course = current_course, id = topic_id)

	current_topic.not_deleted = False
	current_topic.save()

	classUrl = getClassUrl(current_course)

	return HttpResponseRedirect(classUrl+"forum/")


