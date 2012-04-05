# from quiz.models.form import QuizForm
from quiz.models import Question, Answer, Quiz
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

# basic page
def quizIndex(request):
	ques = Question.objects.all()
#	return render_to_response("index.html", context_instance=RequestContext(request))		
	return render_to_response("quiz_index.html", {'question_list': ques}, context_instance=RequestContext(request))

# take answers user has chosen
# and see if it is the answer is correct
def submit(request, answer_id):
	ques = Question.objects.all()

# first select the matching address in DB and check if true or false
# check if specific answer is_correct = false or not...
# to find specific answer, .GET that specific one
#	ans = Answer.object.get(question = ques.answer_id)

	return render_to_response("results.html", {'question_list': ques}, context_instance=RequestContext(request))

#def detail(request):
