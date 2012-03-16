#Student Model
from django.db import models
from Instructor.models import Activities
from Main.models import UserProfile

# Create your models here.
class Submissions(models.Model):
	aid = models.ForeignKey(Activities)
	uid = models.ForeignKey(UserProfile)
	submit_date = models.DateTimeField()
	submit_number = models.IntegerField()
	file_path = models.FileField(upload_to='submissions/%Y/%m/%d') #MAKE SUBMISSION FOLDER IN MEDIA ROOT
	
