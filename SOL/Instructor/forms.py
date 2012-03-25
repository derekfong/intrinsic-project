from django import forms
from django.forms import ModelForm
from Instructor.models import Announcement, Activity, CourseContent
from Gradebook.models import Grade
import datetime

class AnnounceForm(ModelForm):
	#send_email = forms.BooleanField(required=False, label='Send Email?')
	class Meta:
		model = Announcement
		fields = ('title', 'content', )

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
	#	fields = ('uid', 'mark')