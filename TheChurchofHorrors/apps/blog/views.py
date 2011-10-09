# coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def home(request):
    return render_to_response("home.html", context_instance=RequestContext(request))
    
def contact(request):
    return HttpResponse()
    
def staff(request):
    return HttpResponse()
    
def common(request,slug):
    return HttpResponse()
    
def section_subsection(request,section,subsubsection):
    return HttpResponse()
    
def entry(request,section,subsubsection,entry):
    return HttpResponse()
    
def archive(request,year,month):
    return HttpResponse()
    
    
