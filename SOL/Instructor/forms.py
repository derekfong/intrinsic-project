from django import forms
from django.forms import ModelForm
from Instructor.models import Announcement, Activity
import datetime

class AnnounceForm(ModelForm):
	class Meta:
		model = Announcement
		fields = ('title', 'content')

class ActivityForm(ModelForm):
	class Meta:
		model = Activity
		exclude = ('cid',)
