# coding=utf-8

from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.blog.models import Entry,Section,Subsection
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from paginator.paginator import Paginator

def home(request):
    
    right_entries = Entry.get_last_by_section()
    
    
    paginator = Paginator(Entry.get_last(),settings.BLOG_HOME_LAST_ENTRIES,request.GET.get("p",1))
    entries = paginator.current()
    
    return render_to_response("home.html", 
        dict(right_entries=right_entries, entries=entries,paginator=paginator,section=None,subsection=None), 
        context_instance=RequestContext(request))
    
def contact(request):
    
    right_entries = Entry.get_last_by_section()

    return render_to_response("contact.html", 
        dict(right_entries=right_entries, section=None,subsection=None), 
        context_instance=RequestContext(request))
    
def staff(request):
    from userprofile.models import UserProfile,Rol
    
    right_entries = Entry.get_last_by_section()

    rols = Rol.get_all().values_list('name',flat=True)

    return render_to_response("staff.html", 
        dict(right_entries=right_entries, section=None,subsection=None,rols=rols,staffs=UserProfile.get_by_rol()), 
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
    
    paginator = Paginator(Entry.get_last(subsection__id=subsection.id,section__id=section.id),settings.BLOG_OTHER_LAST_ENTRIES,request.GET.get("p",1))
    entries = paginator.current()
    
    right_entries = Entry.get_last_by_section()

    return render_to_response("home.html", 
        dict(right_entries=right_entries, entries=entries,paginator=paginator,section=section,subsection=subsection), 
        context_instance=RequestContext(request))
    
def entry(request,section,subsubsection,entry):
    return HttpResponse()
    
def archive(request,year,month):
    right_entries = Entry.get_last_by_section()

    return render_to_response("archive.html", 
        dict(right_entries=right_entries, section=None,subsection=None), 
        context_instance=RequestContext(request))
    
def author(request,user):
    
    author = get_object_or_404(User,username=user)
    
    entries = Entry.get_last_by_author(author)

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
    
    right_entries = Entry.get_last_by_section()
    
    paginator = Paginator(Entry.get_last(subsection__id=subsection.id),settings.BLOG_OTHER_LAST_ENTRIES,request.GET.get("p",1))
    entries = paginator.current()

    return render_to_response("home-short.html", 
        dict(right_entries=right_entries, entries=entries,paginator=paginator,subsection=subsection,section=None), 
        context_instance=RequestContext(request))

def view_for_section(request,section):
       
    right_entries = Entry.get_last_by_section(section=section)
    
    paginator = Paginator(Entry.get_last(section__id=section.id),settings.BLOG_OTHER_LAST_ENTRIES,request.GET.get("p",1))
    entries = paginator.current()

    return render_to_response("home-short.html", 
        dict(right_entries=right_entries, entries=entries, paginator=paginator,section = section,subsection=None), 
        context_instance=RequestContext(request))
    
    
    
