from django.db import models
from SOL.Main.models import Course

"""
schema for courses 
	cid = models.AutoField(primary_key=True)
	class_name = models.CharField(max_length=256)
	class_number = models.CharField(max_length=3) # 225 of cmpt
	department = models.CharField(max_length=4, choices=FACULTY_DEPT)
	semester = models.CharField(max_length=16, choices=SEMESTER_CHOICES)
	year = models.IntegerField(choices=YEAR_CHOICES)
	section = models.CharField(max_length=4)
"""



# topics created per course...
class Topics(models.Model):
	topic_name = models.CharField(max_length = 125)
	course = models.ForeignKey(Course)
	# if show is false, means it is deleted
	not_deleted = models.BooleanField(default = True) 

	def __unicode__(self):
		return self.topic_name

class Messages(models.Model):
	topic = models.ForeignKey(Topics)	# list of msgs for a topic
	user = models.CharField(max_length=100)	# user who posted
	# need to have a post number for that course ??
	creation_date = models.DateTimeField(auto_now_add = True)
	message = models.TextField()		# the actual message content itself

	# if show is false, means it is deleted
	not_deleted = models.BooleanField(default = True) 
	
	
	def __unicode__(self):
		return self.message

