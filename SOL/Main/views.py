from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth
from Main.models import Course

# Create your views here.
def index(request):
	user = request.user
	class_list = Course.objects.filter(classlist__uid=user.id)
	return render_to_response('main/index.html', {'class_list': class_list},
		context_instance=RequestContext(request))

def logout_view(request):
	auth.logout(request)
	return HttpResponseRedirect("/")
	
#def class_view(request):
	#class = get_object_or_404(Course, )