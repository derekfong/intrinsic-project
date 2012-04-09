from django import forms
from django.forms import ModelForm
from Calendar.models import Event, Label
import datetime

# Create your models here.
class EventForm(ModelForm):
	class Meta:
		model = Event
		exclude = ('uid', 'cid',)

class LabelForm(ModelForm):
	class Meta:
		model = Label
		exclude = ('cid',)
		
class CalendarForm(forms.Form):
	MONTH_CHOICES = (
		(1, u'January'),
		(2, u'February'),
		(3, u'March'),
		(4, u'April'),
		(5, u'May'),
		(6, u'June'),
		(7, u'July'),
		(8, u'August'),
		(9, u'September'),
		(10, u'October'),
		(11, u'November'),
		(12, u'December'),
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
	
	month = forms.ChoiceField(choices=MONTH_CHOICES, initial=datetime.datetime.now().month)
	year = forms.ChoiceField(choices=YEAR_CHOICES, initial=datetime.datetime.now().year)