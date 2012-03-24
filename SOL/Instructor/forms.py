from django import forms
from django.forms import ModelForm
from Instructor.models import Announcement, Activity, CourseContent
from Gradebook.models import Grade
import datetime

# Limits the Annoucement form to render only the 'title' and 'content' fields
class AnnounceForm(ModelForm):
	class Meta:
		model = Announcement
		fields = ('title', 'content')

# Excludes the 'cid' field from the Activity model
class ActivityForm(ModelForm):
	class Meta:
		model = Activity
		exclude = ('cid',)

# Excludes the 'cid' field from the CourseContent model
class CourseForm(ModelForm):
	class Meta:
		model = CourseContent
		exclude = ('cid',)

# Excludes the 'cid' field from the Activity model
class GradeForm(ModelForm):
	class Meta:
		model = Grade
	#	fields = ('uid', 'mark')
