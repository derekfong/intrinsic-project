#Calendar Model
from django.db import models
from Instructor.models import Activities

# Create your models here.
class Events(models.Model):
	eid = models.AutoField(primary_key=True)
	uid = models.ForeignKey(Activities)
	event_name = models.CharField(max_length=256)
	date = models.DateTimeField()
	location = models.CharField(max_length=256)
	