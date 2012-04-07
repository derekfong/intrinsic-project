# forms.py 
from django import forms
from quiz.models import *

# this 
class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		exclude = ('quiz',)
	

