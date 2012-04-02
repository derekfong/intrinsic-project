from django import forms
from django.forms import ModelForm
from Student.models import Submission

class SubmissionForm(ModelForm):
	class Meta:
		model = Submission
		exclude = ('aid', 'uid', 'submit_date', 'submit_number')

