#Gradebook Model
from django.db import models
from Instructor.models import Activities
from Main.models import UserProfile

# Create your models here.
class Grades(models.Model):
	gid = models.AutoField(primary_key=True)
	aid = models.ForeignKey(Activities)
	uid = models.ForeignKey(UserProfile)
	mark = models.DecimalField()

class GradeComment(models.Model):
	gid = models.ForeignKey(Grades)
	description = models.CharField(max_length=256)
	comment = model.TextField()
	