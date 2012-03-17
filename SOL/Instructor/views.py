from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.
def index(request, course_id):
	return render_to_response('instructor/index.html',{'cid': course_id},context_instance=RequestContext(request))
	
