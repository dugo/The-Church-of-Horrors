# coding=utf-8

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from django.template.defaultfilters import slugify
from django.conf import settings
from filebrowser.fields import FileBrowseField

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
        self.slug = slugify(self.name)
        super(type(self),self).save(*args,**kwargs)

class Subsection(models.Model):
    name = models.CharField(_(u"Nombre"),max_length=255,unique=True,db_index=True,blank=False)
    slug = models.SlugField(max_length=255,unique=True,blank=True,help_text=u"Será generada automaticamente a partir del nombre")
    
    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _(u"categoría")
        verbose_name_plural = _(u"categorías")
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
    title = models.CharField(_(u"Título"),max_length=1024,blank=False)
    content = tinymce_models.HTMLField(_("Contenido"),blank=False)
    #brief = models.TextField(_("Brief"),blank=False)
    author = models.ForeignKey(User,verbose_name=_(u"Autor"))
    section = models.ForeignKey(Section,verbose_name=_(u"Sección"))
    subsection = models.ForeignKey(Subsection,verbose_name=_(u"Categoría"))
    created = models.DateTimeField(_(u'Creado'),auto_now_add=True)
    modified = models.DateTimeField(_(u'Modificado'),auto_now=True)
    published = models.BooleanField(_(u'Publicado'),default=False,blank=False)
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
    def get_last(self):
        
        return Entry.objects.order_by('-created')
        
    @classmethod
    def get_last_by_author(self,author,max=settings.BLOG_MAX_LAST_ENTRIES):
        
        return Entry.objects.filter(published=True,author__id=author.id).order_by('-created')[:max]
    
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
                    query = Entry.objects.filter( q ).filter(section__id=s.id)
                    if query.count()>0:
                        entries[unicode(s)] = query[:max]
            else:
                query = Entry.objects.filter( q ).filter(section__id=s.id)
                if query.count()>0:
                    entries[unicode(s)] = query[:max]
        
        return entries
        
    def get_main_image(self):
        print self.images.count()
        return unicode(self.images.get(main=True))
        

class ImageGallery(models.Model):
    entry = models.ForeignKey(Entry,verbose_name=_(u"Entrada"),related_name="images")
    file = FileBrowseField(blank=False,directory='images/%Y/%m',extensions=[".jpg",".png",".jpeg",".gif"])
    order = models.PositiveIntegerField(_(u'Orden'))
    main = models.BooleanField(_(u'Principal'))
    
    def __unicode__(self):
		return unicode(self.file)
    
    class Meta:
        verbose_name = _(u"Imagen de galería")
        verbose_name_plural = _(u"Imagenes de galería")
        ordering = ('order',)
        unique_together = ('entry','order',)
    
    
    
    
    
    
