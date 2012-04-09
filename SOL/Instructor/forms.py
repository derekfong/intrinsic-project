from django import forms
from django.forms import ModelForm
from Instructor.models import Announcement, Quiz, Activity, CourseContent, Slide, Greeting
from Main.models import Setting
from Gradebook.models import Grade
import datetime

## this file creates forms from models provided by Django
class GreetingsForm(ModelForm):
	class Meta:
		model = Greeting
		exclude = ('cid')
class AnnounceForm(ModelForm):
	class Meta:
		model = Announcement
		fields = ('title', 'content', 'send_email' )

class ActivityForm(ModelForm):
	class Meta:
		model = Activity
		exclude = ('cid',)
	def clean_worth(self):
		worth = self.cleaned_data["worth"]
		cid = self.instance.cid
		aid = self.instance.aid

		totalWorth = 0
		activities = Activity.objects.filter(cid=cid).exclude(aid=aid)
		for activity in activities:
			totalWorth += activity.worth
		if totalWorth + worth > 100:
			raise forms.ValidationError("Combined assignments cannot be worth more than 100%.")
		else:
			return worth
		
class CourseForm(ModelForm):
	class Meta:
		model = CourseContent
		exclude = ('cid', 'was_updated', 'updated_on', 'created_on')

class QuizForm(ModelForm):
	class Meta:
		model = Quiz
		exclude = ('cid')
	#def clean_name(self):
	#	name = self.cleaned_data["name"]
	#	try:
	#		Quiz.objects.get(name=name)
	#	except Quiz.DoesNotExist:
	#		return name

	#	raise forms.ValidationError("A quiz with that name already exists.")

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
