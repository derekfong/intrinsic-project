#Calendar Model
from django.db import models
from django.forms import ModelForm
from Main.models import UserProfile
from Instructor.models import Activity

# Create your models here.
class Label(models.Model):
	COLOR_CHOICES = (
		(u'Red', u'Red'),
		(u'Orange', u'Orange'),
		(u'Yellow', u'Yellow'),
		(u'Green', u'Green'),
		(u'Dark Blue', u'Dark Blue'),
		(u'Light Blue', u'Light Blue'),
		(u'Purple', u'Purple'),
		(u'Black', u'Black'),
		(u'Gray', u'Gray'),
	)
	
	lid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=256)
	color = models.CharField(max_length=32, choices=COLOR_CHOICES)
	cid = models.IntegerField(blank=True, null=True)
	def __unicode__(self):
		return '(' + self.color +') '+ self.name

class Event(models.Model):	
	eid = models.AutoField(primary_key=True)
	lid = models.ForeignKey(Label, verbose_name='Label')
	uid = models.ForeignKey(UserProfile, verbose_name='SFU ID')
	cid = models.IntegerField(blank=True, null=True)
	event_name = models.CharField(max_length=64)
	date = models.DateTimeField()
	location = models.CharField(max_length=64, blank=True)
	description = models.TextField(blank=True)
