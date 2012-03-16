#Main Models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#class UserProfile(models.Model)

class Courses(models.Model):
	cid = models.AutoField(primary_key=True)
	class_name = models.CharField(max_length=256)
	class_number = models.IntegerField()
	department = models.CharField(max_length=4)
	faculty = models.CharField(max_length=256)
	semester = models.CharField(max_length=16)
	
class ClassList(models.Model):
	uid = models.ForeignKey(UserProfile)
	cid = models.ForeignKey(Courses)
	is_instructor = models.BooleanField()
	

	
	