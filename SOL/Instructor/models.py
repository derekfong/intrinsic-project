#Instructor Model
from django.db import models
from Main.models import UserProfile, Course

# Create your models here.
class CourseContent(models.Model):
	cid = models.ForeignKey(Course, verbose_name="Course")
	officeHrs = models.CharField(max_length=128, verbose_name="Office Hours")
	officeLocation = models.CharField(max_length=128, verbose_name="Office Location")
	phoneNumber = models.CharField(max_length=12, verbose_name="Phone Number")
	TaOfficeLocation = models.CharField(max_length=128, verbose_name="TA Office Locat")
	TaOfficeHrs = models.CharField(max_length=128, verbose_name="TA's Ofice Hours")
	lectTime = models.CharField(max_length=128, verbose_name="Lecture Time")
	prereq = models.CharField(max_length=128, verbose_name="Prerequisites")
	books = models.TextField(verbose_name="Books")
	topics = models.TextField(verbose_name="Topics Covered")
	markingScheme = models.TextField(verbose_name="Marking Scheme")
	academicHonesty = models.TextField(verbose_name="Academic Honesty")
	additionalInfo = models.TextField(blank=True, verbose_name="Additional Info")
	created_on = models.DateTimeField()
	was_updated = models.BooleanField(default=0)
	updated_on = models.DateTimeField()
	file_path = models.FileField(upload_to='syllabus', blank=True, verbose_name="Upload Syllabus") #MAKE SUBMISSION FOLDER IN MEDIA ROOT
	
class Slide(models.Model):
	cid = models.ForeignKey(Course, verbose_name="Course")
	title = models.CharField(max_length=128)
	uploaded_on = models.DateTimeField()
	file_path = models.FileField(upload_to='slides')

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