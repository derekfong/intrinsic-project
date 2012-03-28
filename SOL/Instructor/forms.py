from django import forms
from django.forms import ModelForm
from Instructor.models import Announcement, Activity, CourseContent, Slide
from Main.models import Setting
from Gradebook.models import Grade
import datetime

## this file overrides the built-in forms provided by Django

class AnnounceForm(ModelForm):
	class Meta:
		model = Announcement
		fields = ('title', 'content', 'send_email' )

class ActivityForm(ModelForm):
	class Meta:
		model = Activity
		exclude = ('cid',)
		
class CourseForm(ModelForm):
	class Meta:
		model = CourseContent
		exclude = ('cid', 'was_updated', 'updated_on', 'created_on')

class GradeForm(ModelForm):
	class Meta:
		model = Grade
	
class SlideForm(ModelForm):
	class Meta:
		model = Slide
		exclude = ('cid', 'uploaded_on')
		
class SettingForm(ModelForm):
	class Meta:
		model = Setting
		exclude = ['uid']
