# coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.blog.models import Entry
import time,random

def home(request):
    
    random.seed(time.time())
    
    right_entries = Entry.get_last_by_section(request.user)
    gallery_entries = Entry.get_home_gallery()
    entries = Entry.get_last()[:6]
    
    random.shuffle(entries)
    random.shuffle(gallery_entries)

    return render_to_response("home.html", 
        dict(right_entries=right_entries, entries=entries), 
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
    
def author(request,user):
    return HttpResponse(user)
    
    
