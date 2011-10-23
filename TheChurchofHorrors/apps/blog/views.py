# coding=utf-8

from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.blog.models import Entry,Section,Subsection
import time,random
from django.conf import settings

def home(request):
    
    random.seed(time.time())
    
    right_entries = Entry.get_last_by_section(request.user)
    gallery_entries = list(Entry.get_home_gallery())
    entries = list(Entry.get_last()[:settings.BLOG_MAX_LAST_ENTRIES])
    
    random.shuffle(entries)
    random.shuffle(gallery_entries)

    return render_to_response("home.html", 
        dict(right_entries=right_entries, entries=entries,show_long=True), 
        context_instance=RequestContext(request))
    
def contact(request):
    return HttpResponse()
    
def staff(request):
    return HttpResponse()
    
def common(request,slug):
    
    try:
        return view_for_entry( request, Entry.objects.get(slug=slug) )
    except Entry.DoesNotExist:
        pass

    try:
        return view_for_subsection( request, subsection = Subsection.objects.get(slug=slug) )
    except Subsection.DoesNotExist:
        pass

    try:
        return view_for_section( request, section = Section.objects.get(slug=slug) )
    except Section.DoesNotExist:
        return HttpResponseNotFound()

    return HttpResponseNotFound()
    
def section_subsection(request,section,subsubsection):
    return HttpResponse()
    
def entry(request,section,subsubsection,entry):
    return HttpResponse()
    
def archive(request,year,month):
    return HttpResponse()
    
def author(request,user):
    return HttpResponse(user)


def view_for_entry(request,entry):
    
    right_entries = Entry.get_last_by_author(entry.author)
    

    return render_to_response("entry.html", 
        dict(right_entries=right_entries, entry=entry), 
        context_instance=RequestContext(request))
        
def view_for_subsection(request,subsection):
    
    entries = list(Entry.get_last(subsection__id=subsection.id)[:settings.BLOG_MAX_LAST_ENTRIES])
    right_entries = Entry.get_last_by_section(request.user)

    random.shuffle(entries)

    return render_to_response("home.html", 
        dict(right_entries=right_entries, entries=entries, show_long=False), 
        context_instance=RequestContext(request))

def view_for_section(request,section):
    
    entries = list(Entry.get_last(section__id=section.id)[:settings.BLOG_MAX_LAST_ENTRIES])
    right_entries = Entry.get_last_by_section(request.user,section=section)

    random.shuffle(entries)

    return render_to_response("home.html", 
        dict(right_entries=right_entries, entries=entries, show_long=False), 
        context_instance=RequestContext(request))
    
    
    
