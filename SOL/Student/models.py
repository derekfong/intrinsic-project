#Student Model
from django.db import models
from Instructor.models import Activity
from Main.models import UserProfile

# Create your models here.
class Submission(models.Model):
	aid = models.ForeignKey(Activity, verbose_name="Activity") #Activity is general overview of activity e.g. the weight, due date, status, name, etc
	uid = models.ForeignKey(UserProfile, verbose_name="User")
	submit_date = models.DateTimeField()
	submit_number = models.IntegerField()	# num of times an assn is submitted
	file_path = models.FileField(upload_to='submissions/%Y/%m/%d') #MAKE SUBMISSION FOLDER IN MEDIA ROOT
	
