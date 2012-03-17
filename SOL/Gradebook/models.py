#Gradebook Model
from django.db import models
from Instructor.models import Activity
from Main.models import UserProfile

# Create your models here.
class Grade(models.Model):
	gid = models.AutoField(primary_key=True)
	aid = models.ForeignKey(Activity)
	uid = models.ForeignKey(UserProfile)
	mark = models.DecimalField(decimal_places=2, max_digits=10)

class GradeComment(models.Model):
	gid = models.ForeignKey(Grade)
	description = models.CharField(max_length=256)
	comment = models.TextField()
	