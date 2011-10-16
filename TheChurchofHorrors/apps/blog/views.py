# coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.blog.models import Entry
import time,random

def home(request):
    
    random.seed(time.time())
    
    right_entries = Entry.get_last_by_section(request.user)
    content_entries = list(Entry.get_last()[:6])
    content_entries = random.shuffle(content_entries)

    return render_to_response("home.html", 
        dict(right_entries=right_entries, content_entries=content_entries), 
        context_instance=RequestContext(request))
    
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
    
    
