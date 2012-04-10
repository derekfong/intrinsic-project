# Create your views here.
from board.models import *
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

# this will go to the course
def index(request):
	# one message board per course (for that semseter)
	courses = Overview.objects.all()

	return render_to_response("index.html", {'courses': courses}, context_instance=RequestContext(request))


# choose which topic to view
def topic_display(request, course_id):

	# list all topics of a course
	topics = Topics.objects.filter(course = course_id)
	
	course = Overview.objects.get(id = course_id)

	# bottom of page, user can post a new topic AND a new corresponding message
	# post given: title, user, and message
	if request.method == 'POST':
		user_topic = Topics(topic_name = request.POST['title'], course = course)
		user_topic.save()

		new_topic = Topics.objects.get(topic_name = request.POST['title'], course=course, id=user_topic.id)

		# use new topic id that was just created
		user_post = Messages(topic = new_topic, user = request.POST['user'], message = request.POST['message'])
		user_post.save()

	return render_to_response("topic_display.html", {'course': course_id, 'topics': topics}, context_instance=RequestContext(request))



# list out all messages for that course
def message_display(request, course_id, topic_id):
 
	# get all the msgs relating to the specific topic_id
	msgs = Messages.objects.filter(topic = topic_id)

	# this is for inserting post into database (see below)
	# use course_id and topic_id as a superkey
	current_topic = Topics.objects.get(course = course_id, id = topic_id)

	# at bottom of page, user will post their reply/entry
	# model names avail: topic, user, and message
	# user = user.request
	if request.method == 'POST':
		# user = request.user
		# save the message user has given
		user_post = Messages(topic = current_topic, user = request.POST['user'], message = request.POST['message'])
		user_post.save()
	

	return render_to_response("message_display.html", {'messages': msgs,}, context_instance=RequestContext(request))
