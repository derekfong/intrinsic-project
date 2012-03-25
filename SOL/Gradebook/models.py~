#Gradebook Model
from django.db import models
from Instructor.models import Activity
from Main.models import UserProfile, ClassList
from django import forms

# Create your models here.
class Grade(models.Model):
	gid = models.AutoField(primary_key=True)
	aid = models.ForeignKey(Activity, verbose_name='Assignment')
	uid = models.ForeignKey(UserProfile, verbose_name='Student')
	mark = models.DecimalField(decimal_places=2, max_digits=10)

class GradeComment(models.Model):
	gid = models.ForeignKey(Grade)
	description = models.CharField(max_length=256)
	comment = models.TextField()

class UploadGrade(forms.Form):
    def __init__(self, *args, **kwargs):
		cid=kwargs.pop('cid')
		super(UploadGrade, self).__init__(*args, **kwargs)
		self.fields['activity_name'] = forms.ModelChoiceField(queryset=Activity.objects.filter(cid=cid), empty_label="<Choose Activity>")
		self.fields['file_path'] = forms.FileField()

		
