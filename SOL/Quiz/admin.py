from quiz.models import *
from django.contrib import admin

class QuizAdmin(admin.ModelAdmin):
	pass

class QuestionAdmin(admin.ModelAdmin):
	pass

class AnswerAdmin(admin.ModelAdmin):
	pass

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
