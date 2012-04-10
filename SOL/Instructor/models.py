#Instructor Model
from django.db import models
from Main.models import UserProfile, Course
from django.forms.models import ModelChoiceField
import os

# Create your models here.
class CourseContent(models.Model):
	#verbose name is just anothr label to use it as
	# below info will be filled in on website by prof
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
		# syllabus will be dl'able as pdf, hence media rot needed	

class Greeting(models.Model):
	cid = models.ForeignKey(Course, verbose_name="Course")
	message = models.TextField(verbose_name="Greeting")
	
class Quiz(models.Model):
	cid = models.ForeignKey(Course, verbose_name="Course")
	name = models.CharField(max_length=256)
	start_date = models.DateTimeField(verbose_name="Start Date")
	end_date = models.DateTimeField(verbose_name="End Date")
	student_attempts = models.IntegerField(verbose_name="Student Attempts")
	def __unicode__(self):
		return self.name

class QuizQuestion(models.Model):
	ANSWER_CHOICES = (
		(0, u'A'),
		(1, u'B'),
		(2, u'C'),
		(3, u'D'),
	)
	qid = models.ForeignKey(Quiz, verbose_name="Quiz")
	question = models.CharField(max_length=512)
	option1 = models.CharField(max_length=512, verbose_name="Option A")
	option2 = models.CharField(max_length=512, verbose_name="Option B")
	option3 = models.CharField(max_length=512, verbose_name="Option C")
	option4 = models.CharField(max_length=512, verbose_name="Option D")
	answer = models.IntegerField(choices=ANSWER_CHOICES)
	#def __init__(self, *args, **kwargs):
	#	qid=kwargs.pop('qid')
	#	super(QuizQuestion, self).__init__(*args, **kwargs)
	#	self.fields['name'] = ActivityModelChoiceField(queryset=Quiz.objects.get(id=qid), empty_label="<Choose Quiz>")

def get_slide_path(instance, file_name):
	course = instance.cid

	year = str(course.year)
	semester = course.semester
	department = course.department
	class_number = course.class_number
	section = course.section

	return os.path.join('slides', year, semester, department, class_number, section, file_name)

class Slide(models.Model):
	#slide is the lecture notes
	cid = models.ForeignKey(Course, verbose_name="Course")
	title = models.CharField(max_length=128)
	uploaded_on = models.DateTimeField()
	file_path = models.FileField(upload_to=get_slide_path, verbose_name="Select File")

class Activity(models.Model):
	# Activity is an assn, midterm, exam, checkpoint, etc of a course
	STATUS_CHOICES = (
		(0, u'Not Marked'),
		(1, u'Marked but not Released'),
		(2, u'Marked and Released'),
	)
	
	FILE_TYPES = (
		(u'No Submission', u'No Submission'),
		(u'.pdf', u'Portable Document Format (.pdf)'),
		(u'.doc', u'Word 2003 Document (.doc)'),
		(u'.docx', u'Word 2007,2010 Document (.docx)'),
		(u'.txt', u'Text Document (.txt)'),
		(u'.zip', u'Multiple Documents (.zip)'),
	)
	
	aid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Course, verbose_name="Class")
	activity_name = models.CharField(max_length=256, verbose_name="Activity Name")
	out_of = models.DecimalField(decimal_places=2, max_digits=5)
	worth = models.IntegerField()
	due_date = models.DateTimeField()
	submission_file_type = models.CharField(max_length=64, choices=FILE_TYPES)
	description = models.TextField(blank=True)
	description_doc = models.FileField(upload_to='descriptions', blank=True, verbose_name="Add Description")
	status = models.IntegerField(choices=STATUS_CHOICES)
	def __unicode__(self):
		return u"%s"%self.cid+" "+self.activity_name
	
class Announcement(models.Model):
	# messages from instructor/TA that will show up on site
	anid = models.AutoField(primary_key=True)
	cid = models.ForeignKey(Course, verbose_name='Class')
	uid = models.ForeignKey(UserProfile, verbose_name='User', related_name='uid')
	title = models.CharField(max_length=256)
	content = models.TextField()
	date_posted = models.DateTimeField()
	send_email = models.BooleanField(default=False, verbose_name="Send Email?")
	was_updated = models.BooleanField(default=0)
	updated_by = models.ForeignKey(UserProfile, related_name='updated_by')
	updated_on = models.DateTimeField(blank=True)
	
class AnnounceRead(models.Model):
	# makes note of whether an annoucement is read or not
	anid = models.ForeignKey(Announcement)
	uid = models.ForeignKey(UserProfile)
	read = models.BooleanField()
	
class ActivityModelChoiceField(ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.name
		
#class Content (CMS??????)
