#Calendar Model
from django.db import models
from Instructor.models import Activity

# Create your models here.
class Event(models.Model):
	eid = models.AutoField(primary_key=True)
	uid = models.ForeignKey(Activity)
	event_name = models.CharField(max_length=256)
	date = models.DateTimeField()
	location = models.CharField(max_length=256)
	