# coding=utf-8

from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.blog.models import Entry,Section,Subsection
import time,random
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User

def home(request):
    
    random.seed(time.time())
    
    right_entries = Entry.get_last_by_section(request.user)
    entries = list(Entry.get_last()[:settings.BLOG_MAX_LAST_ENTRIES])
    
    #random.shuffle(entries)

    return render_to_response("home.html", 
        dict(right_entries=right_entries, entries=entries,section=None,subsection=None), 
        context_instance=RequestContext(request))
    
def contact(request):
    
    right_entries = Entry.get_last_by_section(request.user)

    return render_to_response("contact.html", 
        dict(right_entries=right_entries, section=None,subsection=None), 
        context_instance=RequestContext(request))
    
def staff(request):
    right_entries = Entry.get_last_by_section(request.user)

    return render_to_response("staff.html", 
        dict(right_entries=right_entries, section=None,subsection=None), 
        context_instance=RequestContext(request))
    
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
    
def section_subsection(request,section,subsection):
    
    section = get_object_or_404(Section,slug=section)
    subsection = get_object_or_404(Subsection,slug=subsection)
    
    entries = list(Entry.get_last(subsection__id=subsection.id,section__id=section.id)[:settings.BLOG_MAX_LAST_ENTRIES])
    
    right_entries = Entry.get_last_by_section(request.user)

    #random.shuffle(entries)

    return render_to_response("home.html", 
        dict(right_entries=right_entries, entries=entries,section=section,subsection=subsection), 
        context_instance=RequestContext(request))
    
def entry(request,section,subsubsection,entry):
    return HttpResponse()
    
def archive(request,year,month):
    right_entries = Entry.get_last_by_section(request.user)

    return render_to_response("archive.html", 
        dict(right_entries=right_entries, section=None,subsection=None), 
        context_instance=RequestContext(request))
    
def author(request,user):
    
    author = get_object_or_404(User,username=user)
    
    #right_entries = Entry.get_last_by_section(request.user)
    entries = list(Entry.get_last_by_author(author))

    #random.seed(time.time())
    #random.shuffle(entries)

    return render_to_response("author.html", 
        dict(right_entries=[], entries=entries, author=author,section=None,subsection=None), 
        context_instance=RequestContext(request))


def view_for_entry(request,entry):
    
    if not request.user.is_superuser and not entry.published and (not request.user.is_authenticated() or entry.author_id <> request.user.id):
        return HttpResponseNotFound()
    
    right_entries = Entry.get_last_by_author(entry.author,entry)
    

    return render_to_response("entry.html", 
        dict(right_entries=right_entries, entry=entry), 
        context_instance=RequestContext(request))
        
def view_for_subsection(request,subsection):
    
    entries = list(Entry.get_last(subsection__id=subsection.id)[:settings.BLOG_MAX_LAST_ENTRIES])
    right_entries = Entry.get_last_by_section(request.user)

    #random.shuffle(entries)

    return render_to_response("home-short.html", 
        dict(right_entries=right_entries, entries=entries,subsection=subsection,section=None), 
        context_instance=RequestContext(request))

def view_for_section(request,section):
    
    entries = list(Entry.get_last(section__id=section.id)[:settings.BLOG_MAX_LAST_ENTRIES])
    right_entries = Entry.get_last_by_section(request.user,section=section)

    #random.shuffle(entries)

    return render_to_response("home-short.html", 
        dict(right_entries=right_entries, entries=entries, section = section,subsection=None), 
        context_instance=RequestContext(request))
    
    
    
