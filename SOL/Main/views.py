from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import auth

# Create your views here.
def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))

def logout_view(request):
	auth.logout(request)
	return HttpResponseRedirect("/")