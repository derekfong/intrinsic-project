# from quiz.models.form import QuizForm
from quiz.models import Question, Answer, Quiz
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from quiz.forms import QuestionForm

# basic page
def quizIndex(request):
	# display all the quizzes that user can select

	quizzes= Quiz.objects.all()
	#for quiz in quiz:
		#print quiz.name

#	currentQuiz = Quiz.objects.filter(pk=1)
	

#	return render_to_response("index.html", context_instance=RequestContext(request))		
#	if request.method == 'POST':
#		form = QuestionForm(request.POST, instance=currentQuiz)	

#		if form.is_valid():
			# get all the questions

	return render_to_response("quizzes.html", {'quizzes': quizzes}, context_instance=RequestContext(request))


# take answers user has chosen
# and see if it is the answer is correct
def view_Questions(request, quiz_id):
	questions = Question.objects.filter(pk=quiz_id)

	quiz = Quiz.objects.filter(pk=quiz_id)

	print request.POST
	

	response = ""

	#.POST['answer'] should return the ID of the answer chosen
	if request.method == 'POST':
			chosen_answer = request.POST['answer']
			#print request.POST['answer']
			#print Answer.objects.get(pk = chosen_answer) 

			correct_answer = Answer.objects.filter(id = )
			print correct_answer			

			# grab question and grab answer...			
			if correct_answer:
				response = "Correct Answer"
			else: 
				response = "Wrong Answer"

	#	if form.is_valid():
			# compare the answers to the answer that's been submitted
			# you have answers 
			#if request.POST.is_correct == TRUE:
			
	#else:
		#form = QuestionForm(instance=questions)
	
	return render_to_response("questions.html", {'questions': questions, 'response': response}, context_instance=RequestContext(request))

			
# first select the matching address in DB and check if true or false
# check if specific answer is_correct = false or not...
# to find specific answer, .GET that specific one
#	ans = Answer.object.get(question = ques.answer_id)

	return render_to_response("results.html", {'question_list': ques}, context_instance=RequestContext(request))

#def detail(request):
