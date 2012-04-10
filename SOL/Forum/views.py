# Create your views here.
from Forum.models import *
from Main.models import Course
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from SOL.Student.views import getClassObject, getClassUrl

"""
# this will go to the course
def index(request):
	# one message board per course (for that semseter)
	courses = Course.objects.all()

	return render_to_response("forum/index.html", {'courses': courses}, context_instance=RequestContext(request))
"""

# choose which topic to view
def topic_display(request, department, class_number, year, semester, section):

	user = request.user
	current_course = getClassObject(department, class_number, year, semester, section, user)

	# list all topics of a course
	topics = Topics.objects.filter(course = current_course.cid)
	classUrl = getClassUrl(current_course)
	
	#course = Overview.objects.get(id = course_id)

	# bottom of page, user can post a new topic AND a new corresponding message
	# post given: title, user, and message

	if request.method == 'POST':
		if len(str(request.POST['title'])) <=1 or len(str(request.POST['message'])) <=1:
			error_message = "Please make sure all fields are filled."

			return render_to_response("forum/topic_display.html", {'error_message': error_message, 'topics': topics, 'classUrl': classUrl,}, context_instance=RequestContext(request))

		else: 

			user_topic = Topics(topic_name = request.POST['title'], course = current_course)
			user_topic.save()

			new_topic = Topics.objects.get(topic_name = request.POST['title'], course=current_course, id=user_topic.id)

			# use new topic id that was just created
			user_post = Messages(topic = new_topic, user = request.user, message = request.POST['message'])
			user_post.save()

			return HttpResponseRedirect(classUrl+"forum/")
	

	return render_to_response("forum/topic_display.html", {'topics': topics, 'classUrl': classUrl,}, context_instance=RequestContext(request))



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

	# at bottom of page, user will post their reply/entry
	# model names avail: topic, user, and message
	# user = user.request
	if request.method == 'POST':
		# user = request.user
		# save the message user has given
		user_post = Messages(topic = current_topic, user = request.user, message = request.POST['message'])
		user_post.save()

	return render_to_response("forum/message_display.html", {'messages': msgs,}, context_instance=RequestContext(request))


