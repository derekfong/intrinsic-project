#Instructor Model
from django.db import models
from Main.models import UserProfile, Course

# Create your models here.
class CourseContent(models.Model):
	cid = models.ForeignKey(Course, verbose_name="Course")
	officeHrs = models.CharField(max_length=128)
	officeLocation = models.CharField(max_length=128)
	phoneNumber = models.CharField(max_length=12)
	TaOfficeLocation = models.CharField(max_length=128)
	TaOfficeHrs = models.CharField(max_length=128)
	lectTime = models.CharField(max_length=128)
	prereq = models.CharField(max_length=128)
	books = models.TextField()
	topics = models.TextField()
	markingScheme = models.TextField()
	academicHonesty = models.TextField()
	additionalInfo = models.TextField()
	file_path = models.FileField(upload_to='syllabus', blank=True) #MAKE SUBMISSION FOLDER IN MEDIA ROOT
	
class Activity(models.Model):
	STATUS_CHOICES = (
		(0, u'Not Marked'),
		(1, u'Marked but not Released'),
		(2, u'Marked and Released'),
	)
	aid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Course, verbose_name="Class")
	activity_name = models.CharField(max_length=256, verbose_name="Activity Name")
	out_of = models.DecimalField(decimal_places=2, max_digits=5)
	worth = models.IntegerField()
	due_date = models.DateTimeField()
	#description = models.TextField()
	status = models.IntegerField(choices=STATUS_CHOICES)
	def __unicode__(self):
		return u"%s"%self.cid+" "+self.activity_name
	
class Announcement(models.Model):
	anid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Course, verbose_name='Class')
	uid = models.ForeignKey(UserProfile, verbose_name='User', related_name='uid')
	title = models.CharField(max_length=256)
	content = models.TextField()
	date_posted = models.DateTimeField()
	was_updated = models.BooleanField(default=0)
	updated_by = models.ForeignKey(UserProfile, related_name='updated_by')
	updated_on = models.DateTimeField(blank=True)
	
class AnnounceRead(models.Model):
	anid = models.ForeignKey(Announcement)
	uid = models.ForeignKey(UserProfile)
	read = models.BooleanField()
	
#class Content (CMS??????)