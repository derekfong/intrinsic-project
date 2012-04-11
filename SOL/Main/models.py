#Main Models
from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	sfu_id = models.IntegerField(unique=True, verbose_name="SFU ID")
	def __unicode__(self):
		return u'%s' %self.sfu_id

class Course(models.Model):
	FACULTY_DEPT = (
		(u'Faculty of Applied Sciences', (
				(u'CMPT', u'Computing Sciences'),
				(u'ENSC', u'Engineering Sciences'),
			)
		),
		(u'Faculty of Arts and Social Sciences', (
				(u'CRIM', u'Criminology'),
				(u'ECON', u'Economics'),
				(u'ENGL', u'English'),
				(u'FREN', u'French'),
				(u'GERO', u'Gerontology'),
				(u'HIST', u'History'),
				(u'HUM', u'Humanities'),
				(u'IS', u'International Studies'),
				(u'LING', u'Linguistics'),
				(u'PHIL', u'Philosophy'),
				(u'POL', u'Political Sciences'),
				(u'PSYC', u'Psychology'),
				(u'SA', u'Sociology & Anthropology'),
			)
		),	
		(u'Faculty of Business Administration', (
				(u'BUS', u'Business Administration'),
				(u'BUEC', u'Business Economics'),
			)
		),
		(u'Faculty of Communication, Art and Technology', (
				(u'CMNS', u'Communications'),
				(u'FPA', u'Contemporary Arts'),
				(u'IAT', u'Interactive Arts & Technology'),
			)
		),
		(u'Faculty of Education', (
				(u'EDUC', u'Education'),
			)
		),
		(u'Faculty of Environment', (
				(u'ARCH', u'Archeology'),
				(u'ENV', u'Environment'),
				(u'EVSC', u'Environmental Sciences'),
				(u'GEOG', u'Geography'),
				(u'REM', u'Resource & Environmental Management'),
			)
		),
		(u'Faculty of Health Sciences', (
				(u'HSCI', u'Health Sciences'),
			)
		),
		(u'Faculty of Sciences', (
				(u'BISC', u'Biological Sciences'),
				(u'CHEM', u'Chemisty'),
				(u'EASC', u'Earth Sciences'),
				(u'KIN', u'Kinesiology'),
				(u'MATH', u'Mathematics'),
				(u'MACM', u'Mathematics & Computing Science'),
				(u'MBB', u'Molecular Biology & Biochemistry'),
				(u'PHYS', u'Physics'),
				(u'STAT', u'Statistics & Actuarial Sciences'),
			)
		),
	)
	
	SEMESTER_CHOICES = (
		(u'Spring', u'Spring'),
		(u'Summer', u'Summer'),
		(u'Fall', u'Fall'),
	)
	
	YEAR_CHOICES = (
		(2011, u'2011'),
		(2012, u'2012'),
		(2013, u'2013'),
		(2014, u'2014'),
		(2015, u'2015'),
		(2016, u'2016'),
		(2017, u'2017'),
		(2018, u'2018'),
		(2019, u'2019'),
		(2020, u'2020'),
		(2021, u'2021'),
		(2022, u'2022'),
		(2023, u'2023'),
		(2024, u'2024'),
		(2025, u'2025'),
	)
	
	cid = models.AutoField(primary_key=True)
	class_name = models.CharField(max_length=256)
	class_number = models.CharField(max_length=3)
	department = models.CharField(max_length=4, choices=FACULTY_DEPT)
	semester = models.CharField(max_length=16, choices=SEMESTER_CHOICES)
	year = models.IntegerField(choices=YEAR_CHOICES)
	section = models.CharField(max_length=4)
	
	def __unicode__(self):
		return self.department+self.class_number+" "+self.semester+u'%s' %self.year+" "+self.section
	
	# Create a folder in submissions for the course when the course is created
	def save(self, *args, **kwargs):
		#base_path = '/var/www/intrinsic-project/SOL/media/submissions'
<<<<<<< HEAD
		base_path = '/Users/kevin/Dropbox/intrinsic-project Apr10/SOL/media/submissions'
=======
		base_path = '/home/allison/Desktop/CMPT470/copy/SOL/media/submissions'
>>>>>>> 0ff23bd7a9fb65b84f6bbe5022acd0e5a3ab3e87
		year = str(self.year)
		semester = self.semester
		dept = self.department
		class_number = self.class_number
		section = self.section
		
		try:
			os.makedirs(base_path +'/'+ year +'/'+ semester +'/'+ dept +'/'+ class_number +'/'+ section)
		except:
			return 'Course already exists'
		super(Course, self).save(*args, **kwargs)
	
# generates a list of people within a class
class ClassList(models.Model):
	uid = models.ForeignKey(UserProfile, verbose_name='SFU ID')
	cid = models.ForeignKey(Course, verbose_name='course')
	is_instructor = models.BooleanField(verbose_name='is the instructor?')
	is_ta = models.BooleanField(verbose_name='is a TA?')

# allow admin to upload a userlist through admin UI
# and automatically import it
class UploadUserList(models.Model):
	file_name = models.CharField(max_length=64, verbose_name='File Name')
	upload_date = models.DateTimeField(verbose_name='Date file was uploaded')
	is_imported = models.BooleanField(verbose_name='Already imported?')
	file_path = models.FileField(upload_to='new_users')
	def __unicode__(self):
		return self.file_name

class UploadClassList(models.Model):
	cid = models.ForeignKey(Course, verbose_name='course')
	upload_date = models.DateTimeField(verbose_name='Date class list was uploaded')
	is_enrolled = models.BooleanField(verbose_name='Enrolled students already?')
	file_path = models.FileField(upload_to='enrollment_lists')

## THIS IS for the annoucements for a course	
class Setting(models.Model):
	uid = models.ForeignKey(UserProfile, verbose_name="User")
	email_announcement = models.BooleanField(default=False, verbose_name="Announcements")
	email_activity = models.BooleanField(default=False, verbose_name="Grades Released")

