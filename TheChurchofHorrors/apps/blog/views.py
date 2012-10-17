# coding=utf-8

from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.blog.models import Entry,Section,Subsection
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from paginator.paginator import Paginator
import datetime
from recaptcha_works.decorators import fix_recaptcha_remote_ip
from forms import CommentForm,CommentFormAuthenticated
from taggit.models import Tag

def home(request):

    if request.method == "GET" and request.GET.get("q"):
        return search(request)
    
    right_entries = Entry.get_last_by_section()
    
    
    paginator = Paginator(Entry.get_last(),settings.BLOG_HOME_LAST_ENTRIES,request.GET.get("p",1))
    entries = paginator.current()
    
    template = "home.html" if paginator.page == 1 else "home-short.html"
    
    return render_to_response(template, 
        dict(right_entries=right_entries, entries=entries,paginator=paginator,archive=None,section=None,subsection=None,tag=None), 
        context_instance=RequestContext(request))

def search(request):
    
    q = request.GET.get("q")
        
    paginator = Paginator(Entry.search(q),settings.BLOG_OTHER_LAST_ENTRIES,request.GET.get("p",1))
    entries = paginator.current()
    
    right_entries = Entry.get_last_by_section()



    return render_to_response("home-short.html", 
        dict(right_entries=right_entries, entries=entries,paginator=paginator,archive=None,section=None,subsection=None,tag=None), 
        context_instance=RequestContext(request))

def contact(request):

    right_entries = Entry.get_last_by_section()
    
    if request.method == "POST":
        from forms import ContactForm
        
        form = ContactForm(request.POST)
        
        if form.is_valid():
            from django.core.mail import send_mail

            msg = """Nombre: %s\nEmail: %s\nMensaje:\n%s""" % (form.cleaned_data['name'],form.cleaned_data['email'],form.cleaned_data['message'])

            # send email
            send_mail('[TheChurchofHorrors] Formulario de contacto', msg, settings.BLOG_DEFAULT_SENDER, settings.BLOG_CONTACT_EMAILS, fail_silently=True)
            
            return render_to_response("contact-sent.html", 
                dict(right_entries=right_entries, section=None,subsection=None,next = request.POST.get('next') ), 
                context_instance=RequestContext(request))

    return render_to_response("contact.html", 
        dict(right_entries=right_entries, section=None,subsection=None,next = request.GET.get('next')), 
        context_instance=RequestContext(request))
    
def staff(request):
    from userprofile.models import UserProfile,Rol
    
    right_entries = Entry.get_last_by_section()

    rols = Rol.get_all().values_list('name',flat=True)

    return render_to_response("staff.html", 
        dict(right_entries=right_entries, section=None,subsection=None,rols=rols,staffs=UserProfile.group_by_rol()), 
        context_instance=RequestContext(request))

def info(request):
    
    right_entries = Entry.get_last_by_section()

    return render_to_response("info.html", 
        dict(right_entries=right_entries, section=None,subsection=None,), 
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

def subsection_tag(request,subsection,tag):

    subsection = get_object_or_404(Subsection,slug=subsection)
    tag = get_object_or_404(Tag,slug=tag)

    paginator = Paginator(Entry.get_last(subsection__id=subsection.id,tags__id__in=[tag.id]),settings.BLOG_OTHER_LAST_ENTRIES,request.GET.get("p",1))
    entries = paginator.current()
    right_entries = Entry.get_last_by_section()

    return render_to_response("home-short.html", 
        dict(right_entries=right_entries, entries=entries,paginator=paginator,archive=None,section=None,subsection=subsection,tag=tag), 
        context_instance=RequestContext(request))
    
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

    paginator = Paginator(Entry.get_archive(year,month),settings.BLOG_OTHER_LAST_ENTRIES,request.GET.get("p",1))
    entries = paginator.current()

    return render_to_response("home-short.html", 
        dict(right_entries=right_entries,entries=entries, archive=datetime.date(int(year),int(month),1),section=None,subsection=None,tag=None), 
        context_instance=RequestContext(request))
    
def author(request,user):
    
    author = get_object_or_404(User,username=user)
    
    entries = Entry.get_last_by_author(author)

    return render_to_response("author.html", 
        dict(right_entries=[], entries=entries, author=author,section=None,subsection=None), 
        context_instance=RequestContext(request))

@fix_recaptcha_remote_ip
def view_for_entry(request,entry):
    
    if not request.user.is_superuser and (request.user.is_authenticated() and not request.user.get_profile().is_editor) and not entry.published and (not request.user.is_authenticated() or entry.author_id <> request.user.id):
        return HttpResponseNotFound()
    
    author = website = email = content = ''
    
    if request.method == "POST":
        
        if not request.user.is_authenticated():
            return HttpResponseForbidden()
            
        
        form = CommentFormAuthenticated(request.POST) if request.user.is_authenticated() else CommentForm(request,request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.entry = entry
            comment.time = datetime.datetime.now()
            comment.save()
            
            # send notification
            comment.notify()
            
            #return HttpResponseRedirect("%s#comments" % entry.get_absolute_url() )
        
        else:
            author = request.POST.get("author","")
            website = request.POST.get("website","")
            email = request.POST.get("email","")
            content = request.POST.get("content","")

    else:
        form = CommentFormAuthenticated() if request.user.is_authenticated() else CommentForm(request)
    
    right_entries = Entry.get_last_by_author(entry.author,entry)

    return render_to_response("entry.html", 
        dict(right_entries=right_entries,
            entry=entry,
            author=author,
            website=website,
            email=email,
            content=content,
            form=form), 
        context_instance=RequestContext(request))
        
def view_for_subsection(request,subsection):
    
    right_entries = Entry.get_last_by_section()
    
    paginator = Paginator(Entry.get_last(subsection__id=subsection.id),settings.BLOG_OTHER_LAST_ENTRIES,request.GET.get("p",1))
    entries = paginator.current()

    return render_to_response("home-short.html", 
        dict(right_entries=right_entries, entries=entries,paginator=paginator,archive=None,subsection=subsection,section=None,tag=None), 
        context_instance=RequestContext(request))

def view_for_section(request,section):
       
    right_entries = Entry.get_last_by_section(section=section)
    
    paginator = Paginator(Entry.get_last(section__id=section.id),settings.BLOG_OTHER_LAST_ENTRIES,request.GET.get("p",1))
    entries = paginator.current()

    return render_to_response("home-short.html", 
        dict(right_entries=right_entries, entries=entries, paginator=paginator,section = section,archive=None,subsection=None,tag=None), 
        context_instance=RequestContext(request))

