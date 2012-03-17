#Main Models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	sfu_id = models.IntegerField(unique=True, verbose_name="SFU ID")
	def __unicode__(self):
		return u'%s' %self.sfu_id

class Course(models.Model):
	DEPARTMENT_CHOICES = (
		(u'bisc', u'Biological Sciences'),
		(u'bus', u'Business Administration'),
		(u'chem', u'Chemisty'),
		(u'cmpt', u'Computing Sciences'),
		(u'engl', u'English'),
		(u'easc', u'Earth Sciences'),
		(u'ensc', u'Engineering Sciences'),
		(u'macm', u'Mathematics & Computing Science'),
		(u'math', u'Mathematics'),	
	)
	
	FACULTY_CHOICES = (
		(u'applied sciences', u'Applied Sciences'),
		(u'arts and social sciences', u'Arts and Social Sciences'),	
		(u'business administration', u'Business Administration'),
		(u'communication, art and technology', u'Communication, Art and Technology'),
		(u'education', u'Education'),
		(u'environment', u'Environment'),
		(u'health sciences', u'Health Sciences'),
		(u'sciences', u'Sciences'),
	)
	
	SEMESTER_CHOICES = (
		(u'spring', u'Spring'),
		(u'summer', u'Summer'),
		(u'fall', u'Fall'),
	)
	
	YEAR_CHOICES = (
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
	department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES)
	faculty = models.CharField(max_length=256, choices=FACULTY_CHOICES)
	semester = models.CharField(max_length=16, choices=SEMESTER_CHOICES)
	year = models.IntegerField(choices=YEAR_CHOICES)
	def __unicode__(self):
		return self.department+self.class_number+" "+self.semester+u'%s' %self.year
	
class ClassList(models.Model):
	uid = models.ForeignKey(UserProfile, verbose_name='SFU ID')
	cid = models.ForeignKey(Course, verbose_name='course')
	is_instructor = models.BooleanField(verbose_name='is the instructor?')
	is_ta = models.BooleanField(verbose_name='is a TA?')
	

	
	