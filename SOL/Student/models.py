#Student Model
from django.db import models
from Instructor.models import Activity, Course, Quiz, QuizQuestion
from Main.models import UserProfile
import os

def get_submission_path(instance, file_name):
	activity = instance.aid
	user_profile = instance.uid
	course = activity.cid
	
	year = str(course.year)
	semester = course.semester
	department = course.department
	class_number = course.class_number
	section = course.section
	activity_name = activity.activity_name
	username = user_profile.user.username
	return os.path.join('submissions', year, semester, department, class_number, section, activity_name, username, file_name)

class Submission(models.Model):
	aid = models.ForeignKey(Activity, verbose_name="Activity") #Activity is general overview of activity e.g. the weight, due date, status, name, etc
	uid = models.ForeignKey(UserProfile, verbose_name="User")
	submit_date = models.DateTimeField(auto_now=True, auto_now_add=True)
	submit_number = models.IntegerField()	# num of times an assn is submitted
	file_path = models.FileField(upload_to=get_submission_path)
	
class QuizAttempt(models.Model):
	qid = models.ForeignKey(Quiz, verbose_name="Quiz")
	uid = models.ForeignKey(UserProfile)
	time = models.DateTimeField()
	result = models.IntegerField()

class QuizResult(models.Model):
	attempt = models.ForeignKey(QuizAttempt)
	question = models.ForeignKey(QuizQuestion)
	guess = models.IntegerField()