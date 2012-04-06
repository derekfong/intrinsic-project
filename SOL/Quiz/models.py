from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# create three main models:
# Quiz - can have more than just one quiz but this example will just have the one quiz 
	# (so only one pk/entry in this model)
# Question - foreignkey to quiz
# Answer - foreignkey to question


class Quiz(models.Model):
	name = models.CharField(max_length = 225)
	creation = models.DateField(auto_now_add = True)
	
	def __unicode__(self):
		return self.name

	def possible(self):
		total = 0
		for question in self.question_set.all():
			question.save()
			total += question.value
		return total

class Question(models.Model):
	question = models.CharField(max_length = 255)
	quiz = models.ForeignKey(Quiz) #link a question to a quiz
	creation = models.DateField(auto_now_add = True)
    	#objective = TODO: include standards linking in later versions
	value = models.IntegerField(default = 1)

	def __unicode__(self):
		return self.question

class Answer(models.Model):
	answer = models.CharField(max_length = 255)
	question = models.ForeignKey(Question)
	is_correct = models.BooleanField(default = False)

	def __unicode__(self):
		return self.answer

