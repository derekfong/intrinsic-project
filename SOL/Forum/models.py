from django.db import models

class Overview(models.Model):
	class_name = models.CharField(max_length = 10) # name of course e.g. CMPT 125
	semester = models.CharField(max_length = 10) # e.g. Spring 2012 is 1124
	# should be diff boards for CMPT 125 in burnaby vs CMPT 125 in Surrey

	def __unicode__(self):
		return self.class_name	

# topics created per course...
class Topics(models.Model):
	topic_name = models.CharField(max_length = 125)
	course = models.ForeignKey(Overview)

	def __unicode__(self):
		return self.topic_name

class Messages(models.Model):
	topic = models.ForeignKey(Topics)	# list of msgs for a topic
	user = models.CharField(max_length=125)	# user who posted
	# need to have a post number for that course ??
	creation_date = models.DateField(auto_now_add = True)
	message = models.TextField()		# the actual message content itself
	
	def __unicode__(self):
		return self.message

