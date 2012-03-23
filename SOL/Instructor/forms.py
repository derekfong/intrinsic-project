from django import forms
from django.forms import ModelForm
from Instructor.models import Announcement, Activity, CourseContent
import datetime

class AnnounceForm(ModelForm):
	class Meta:
		model = Announcement
		fields = ('title', 'content')

class ActivityForm(ModelForm):
	class Meta:
		model = Activity
		exclude = ('cid',)
		
class CourseForm(ModelForm):
	class Meta:
		model = CourseContent
		exclude = ('cid',)
