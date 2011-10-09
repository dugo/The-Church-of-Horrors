# coding=utf-8

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from django.template.defaultfilters import slugify
from django.conf import settings

class Section(models.Model):
    name = models.CharField(_(u"Nombre"),max_length=255,unique=True,db_index=True,blank=False)
    slug = models.SlugField(max_length=255,unique=True,blank=True,help_text=u"Será generada automaticamente a partir del nombre")
    
    def __unicode__(self):
        return unicode(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('common', (), {
            'slug': self.slug})
    
    class Meta:
        verbose_name = _(u"sección")
        verbose_name_plural = _(u"secciones")
        ordering = ('name',)

    def save(self,*args,**kwargs):
        if self.name:
            self.name = self.name.upper()
        self.slug = slugify(self.name)
        super(type(self),self).save(*args,**kwargs)

class Subsection(models.Model):
    name = models.CharField(_(u"Nombre"),max_length=255,unique=True,db_index=True,blank=False)
    slug = models.SlugField(max_length=255,unique=True,blank=True,help_text=u"Será generada automaticamente a partir del nombre")
    
    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _(u"subsección")
        verbose_name_plural = _(u"subsecciones")
        ordering = ('name',)

    @models.permalink
    def get_absolute_url(self):
        
        if hasattr(self,"section"):
            return ('section_subsection', (), {
                'section': self.section,
                'subsection': self.slug})
                
        else:
            return ('common', (), {
                'slug': self.slug})
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(type(self),self).save(*args,**kwargs)


class Entry(models.Model):
    content = tinymce_models.HTMLField(_("Contenido"),blank=False)
    brief = models.TextField(_("Brief"),blank=False)
    author = models.ForeignKey(User,verbose_name=_(u"Autor"))
    section = models.ForeignKey(Section,verbose_name=_(u"Sección"))
    subsection = models.ForeignKey(Subsection,verbose_name=_(u"Subsección"))
    created = models.DateTimeField(_(u'Creado'),auto_now_add=True)
    modified = models.DateTimeField(_(u'Modificado'),auto_now=True)
    published = models.BooleanField(_(u'Publicado'),default=False,blank=False)
    title = models.CharField(_(u"Título"),max_length=1024,blank=False)
    slug = models.SlugField(max_length=255,unique=True,blank=True,help_text=u"Será generada automaticamente a partir del título")
    
    def __unicode__(self):
        return unicode(self.title)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(type(self),self).save(*args,**kwargs)

    class Meta:
        verbose_name = _(u"entrada")
        ordering = ('-created',)

    @models.permalink
    def get_absolute_url(self):
        return ('entry', (), {
            'section': self.section.slug,
            'subsection': self.subsection.slug,
            'entry': self.slug})
    
    @classmethod
    def get_last_by_author(self,user,author,max=settings.BLOG_MAX_LAST_ENTRIES):
        
        if user.is_authenticated():
            q = models.Q(published=True) | models.Q(author__id=user.id)
        else:
            q = models.Q(published=True)
        
        return Entry.objects.filter( q ).filter(author__id=author.id).order_by('-created')[:max]
    
    @classmethod    
    def get_last_by_section(self,user,section=None,max=settings.BLOG_MAX_LAST_ENTRIES):
        
        entries = {}
        
        if user.is_authenticated():
            q = models.Q(published=True) | models.Q(author__id=user.id)
        else:
            q = models.Q(published=True)
        
        for s in Section.objects.all()[:]:
            if not section is None:
                if s.id <> section.id:
                    entries[unicode(s)] = Entry.objects.filter( q ).filter(section__id=s.id)[:max]
            else:
                entries[unicode(s)] = Entry.objects.filter( q ).filter(section__id=s.id)[:max]
        
        return entries
        

class ImageGallery(models.Model):
    entry = models.ForeignKey(Entry,verbose_name=_(u"Entrada"),related_name="images")
    file = models.ImageField(blank=False,upload_to='images/%Y/%m')
    order = models.PositiveIntegerField(_(u'Orden'))
    
    class Meta:
        verbose_name = _(u"Imagen de galería")
        verbose_name_plural = _(u"Imagenes de galería")
        ordering = ('order',)
        unique_together = ('entry','order',)
    
    
    
    
    
    
