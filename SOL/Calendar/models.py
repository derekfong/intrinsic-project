#Calendar Model
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

from Main.models import UserProfile
from Instructor.models import Activity

# Create your models here.
class Label(models.Model):
	COLOR_CHOICES = (
		(u'Red', u'Red'),
		(u'Cyan', u'Cyan'),
		(u'Blue', u'Blue'),
		(u'Dark Blue', u'Dark Blue'),
		(u'Light Blue', u'Light Blue'),
		(u'Purple', u'Purple'),
		(u'Yellow', u'Yellow'),
		(u'Lime', u'Lime'),
		(u'Fushsia', u'Fuchsia'),
		(u'Silver', u'Silver'),
		(u'Gray', u'Gray'),
		(u'Black', u'Black'),
		(u'Orange', u'Orange'),
		(u'Brown', u'Brown'),
		(u'Maroon', u'Maroon'),
		(u'Green', u'Green'),
		(u'Olive', u'Olive'),
	)
	
	lid = models.AutoField(primary_key=True)
	name = models.CharField(max_length=256)
	color = models.CharField(max_length=32, choices=COLOR_CHOICES)
	def __unicode__(self):
		return '(' + self.color +') '+ self.name

class Event(models.Model):	
	eid = models.AutoField(primary_key=True)
	lid = models.ForeignKey(Label, verbose_name='Label')
	uid = models.IntegerField(blank=True, null=True)
	cid = models.IntegerField(blank=True, null=True)
	event_name = models.CharField(max_length=64)
	date = models.DateTimeField()
	location = models.CharField(max_length=64, blank=True)
	description = models.TextField(blank=True)
