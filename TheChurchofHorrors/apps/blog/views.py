# coding=utf-8

from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect,HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.blog.models import Entry,Subsection,Number
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from paginator.paginator import Paginator
import datetime,random
from recaptcha_works.decorators import fix_recaptcha_remote_ip
from forms import CommentForm,CommentFormAuthenticated,ContactForm
from userprofile.models import UserProfile,Rol
from taggit.models import Tag
from django.views.decorators.csrf import csrf_exempt

def home(request):

    if request.method == "GET" and request.GET.get("q"):
        return search(request)

    number = Number.get_current()

    return HttpResponseRedirect(number.get_absolute_url())

def number(request,number=None,month=None,year=None):
    
    number = get_object_or_404(Number,number=number,year=year,month=month)
    sitios = number.get_sitios()

    return render_to_response("home.html", 
        dict(number=number,sitios=sitios), 
        context_instance=RequestContext(request))

def subsection(request,number,month,year,subsection):

    number = get_object_or_404(Number,number=number,year=year,month=month)
    subsection = get_object_or_404(Subsection,slug=subsection)
    entries=number.other_entries_random.filter(subsection__id=subsection.id)

    return render_to_response("subsection.html", 
        dict(number=number,subsection=subsection,entries=entries,),
        context_instance=RequestContext(request))

def subsection_global(request,slug):

    subsection = get_object_or_404(Subsection,slug=slug)
    entries=subsection.other_entries_random.filter(subsection__id=subsection.id)

    return render_to_response("subsection.html", 
        dict(subsection=subsection,entries=entries,),
        context_instance=RequestContext(request))

def anteriores(request):

    return render_to_response("anteriores.html", context_instance=RequestContext(request))

def search(request):
    
    q = request.GET.get("q")
        
    paginator = Paginator(Entry.search(q),settings.BLOG_OTHER_LAST_ENTRIES,request.GET.get("p",1))
    entries = paginator.current()


    return render_to_response("home-short.html", 
        dict(entries=entries,paginator=paginator,archive=None,section=None,subsection=None,tag=None), 
        context_instance=RequestContext(request))

def contact(request):
   
    if request.method == "POST":
        
        form = ContactForm(request,request.POST)

        if form.is_valid():
            from django.core.mail import send_mail

            msg = """Nombre: %s\nEmail: %s\nMensaje:\n%s""" % (form.cleaned_data['name'],form.cleaned_data['email'],form.cleaned_data['message'])

            # send email
            send_mail('[TheChurchofHorrors] Formulario de contacto', msg, settings.BLOG_DEFAULT_SENDER, settings.BLOG_CONTACT_EMAILS, fail_silently=True)
            
            return render_to_response("contact-sent.html", 
                dict(section=None,subsection=None,next = request.POST.get('next') ), 
                context_instance=RequestContext(request))

    return render_to_response("contact.html", 
        dict(section=None,subsection=None,form=ContactForm(request),next = request.GET.get('next')), 
        context_instance=RequestContext(request))
    
def staff(request):
    rols = Rol.get_all().values_list('name',flat=True)

    return render_to_response("staff.html", 
        dict(rols=rols,staffs=UserProfile.group_by_rol()), 
        context_instance=RequestContext(request))

def info(request):
    

    return render_to_response("info.html", 
        context_instance=RequestContext(request))
    
def common(request,slug):
    

    try:
        return view_for_subsection( request, subsection = Subsection.objects.get(slug=slug) )
    except Subsection.DoesNotExist:
        pass


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

def authors(request):

    def chunkIt(seq, num):
      avg = len(seq) / float(num)
      out = []
      last = 0.0

      while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

      return out
    
    qs = list(set(UserProfile.get_authors()))
    
    random.shuffle(qs)
    authors = chunkIt(qs,3)
    authors.reverse()
    
    return render_to_response("authors.html", 
        dict(authors=authors,), 
        context_instance=RequestContext(request))

def author(request,user):
    
    author = get_object_or_404(User,username=user)
    
    entries = Entry.get_last_by_author(author)

    return render_to_response("author.html", 
        dict(entries=entries, author=author,), 
        context_instance=RequestContext(request))

@fix_recaptcha_remote_ip
def entry(request,number,month,year,subsection,slug):
    
    number = get_object_or_404(Number,number=number,year=year,month=month)
    entry = get_object_or_404(Entry,number__id=number.id,slug=slug,subsection__slug=subsection)
    
    if not request.user.is_superuser and (request.user.is_authenticated() and not request.user.get_profile().is_editor) and not entry.published and (not request.user.is_authenticated() or entry.author_id <> request.user.id):
        return HttpResponseNotFound()
    
    author = website = email = content = ''
    
    if request.method == "POST":

        
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
        entry.add_view_mark(request.META.get("REMOTE_ADDR"),request.user)
    

    return render_to_response("entry.html", 
        dict(
            entry=entry,
            author=author,
            website=website,
            email=email,
            content=content,
            number=number,
            subsection=entry.subsection,
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


@csrf_exempt
def cookies(request):

    if request.method <> "POST":
        return HttpResponseForbidden()

    request.session['cookiesok'] = True

    return HttpResponse("ok")