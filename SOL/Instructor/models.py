#Instructor Model
from django.db import models
from Main.models import UserProfile, Course

# Create your models here.

class Activity(models.Model):
	STATUS_CHOICES = (
		(0, u'Not Marked'),
		(1, u'Marked but not Released'),
		(2, u'Marked and Released'),
	)
	aid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Course, verbose_name="Class")
	activity_name = models.CharField(max_length=256)
	out_of = models.IntegerField()
	worth = models.IntegerField()
	due_date = models.DateTimeField()
	status = models.IntegerField(choices=STATUS_CHOICES)
	def __unicode__(self):
		return u"%s"%self.cid+" "+self.activity_name
	
class Announcement(models.Model):
	anid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Course, verbose_name='Class')
	uid = models.ForeignKey(UserProfile, verbose_name='User')
	title = models.CharField(max_length=256)
	content = models.TextField()
	date_posted = models.DateTimeField()
	
class AnnounceRead(models.Model):
	anid = models.ForeignKey(Announcement)
	uid = models.ForeignKey(UserProfile)
	read = models.BooleanField()
	
#class Content (CMS??????)