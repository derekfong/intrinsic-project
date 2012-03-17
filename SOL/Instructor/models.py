#Instructor Model
from django.db import models
from Main.models import UserProfile, Course

# Create your models here.
class Activity(models.Model):
	aid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Course)
	activity_name = models.CharField(max_length=256)
	out_of = models.IntegerField()
	worth = models.IntegerField()
	due_date = models.DateTimeField()
	status = models.IntegerField()
	
class Announcement(models.Model):
	anid = models.AutoField(primary_key=True)
	uid = models.ForeignKey(UserProfile)
	content = models.TextField()
	date_posted = models.DateTimeField()
	
class AnnounceRead(models.Model):
	anid = models.ForeignKey(Announcement)
	uid = models.ForeignKey(UserProfile)
	read = models.BooleanField()
	
#class Content (CMS??????)