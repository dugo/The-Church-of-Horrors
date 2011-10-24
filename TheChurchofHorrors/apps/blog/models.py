# coding=utf-8

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from django.template.defaultfilters import slugify
from django.conf import settings
from filebrowser.fields import FileBrowseField
from taggit.managers import TaggableManager


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
                'section': self.section.slug,
                'subsection': self.slug})
                
        else:
            return ('common', (), {
                'slug': self.slug})
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(type(self),self).save(*args,**kwargs)


class Entry(models.Model):
    title = models.CharField(_(u"Título"),max_length=255,blank=False,unique=True)
    content = tinymce_models.HTMLField(_("Contenido"),blank=False,)
    #brief = models.TextField(_("Brief"),blank=False)
    author = models.ForeignKey(User,verbose_name=_(u"Autor"))
    section = models.ForeignKey(Section,verbose_name=_(u"Sección"))
    subsection = models.ForeignKey(Subsection,verbose_name=_(u"Categoría"))
    created = models.DateTimeField(_(u'Creado'),auto_now_add=True)
    modified = models.DateTimeField(_(u'Modificado'),auto_now=True)
    published = models.BooleanField(_(u'Publicado'),default=False,blank=False)
    slug = models.SlugField(max_length=255,unique=True,blank=True,help_text=_(u"Será generada automaticamente a partir del título"))
    gallery = models.BooleanField(_(u'Mostrar en galería de HOME'),help_text=_(u'Se mostrará sólo la imagen marcada cómo principal'),default=False)
    show_gallery = models.BooleanField(_(u'Mostrar galería en entrada'),help_text=_(u'Se mostrará en la propia entrada una galería con las imágenes en el orden establecido'),default=False)
    tags = TaggableManager()
    
    def __unicode__(self):
        return unicode(self.title)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(type(self),self).save(*args,**kwargs)

    class Meta:
        verbose_name = _(u"entrada")
        ordering = ('-created',)

    """@models.permalink
    def get_absolute_url(self):
        return ('entry', (), {
            'section': self.section.slug,
            'subsection': self.subsection.slug,
            'entry': self.slug})"""
    
    @models.permalink
    def get_absolute_url(self):
        return ('common', (), {
            'slug': self.slug})
    
    @classmethod
    def get_last(self,**kwargs):
        
        if kwargs:
            return Entry.objects.order_by('-created').filter(**kwargs).filter(published=True)
        else:
            return Entry.objects.order_by('-created').filter(published=True)
        
    @classmethod
    def get_last_by_author(self,author,max=settings.BLOG_MAX_LAST_ENTRIES):
        
        return Entry.objects.filter(published=True,author__id=author.id).order_by('-created')[:max]
    
    @classmethod
    def get_home_gallery(self):
        
        return Entry.objects.filter(gallery=True).order_by('-created')
    
    @classmethod    
    def get_last_by_section(self,user,section=None,max=settings.BLOG_MAX_LAST_ENTRIES):
        
        entries = {}
        
        # removed!
        if False and user.is_authenticated():
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
        return unicode(self.images.get(main=True))
    
    def get_brief(self):
        import re
        
        content = re.sub(r'<[^>]+>','',self.content)
        
        if len(content) < 300:
            return content
        
        idx = 0
        for i in range(300,450):
            if content[i] == ".":
                idx = i
                break
        else:
            return self.content[:450]
        
        return content[:idx+1]
        

class ImageGallery(models.Model):
    entry = models.ForeignKey(Entry,verbose_name=_(u"Entrada"),related_name="images")
    file = FileBrowseField(blank=False,directory='images/%Y/%m',extensions=[".jpg",".png",".jpeg",".gif"])
    #file = models.ImageField(blank=False,upload_to='images/%Y/%m')
    order = models.PositiveIntegerField(_(u'Orden en la galería'),default=1)
    main = models.BooleanField(_(u'Usar como principal'))
    
    def __unicode__(self):
		return unicode(self.file)
    
    class Meta:
        verbose_name = _(u"Imagen de galería")
        verbose_name_plural = _(u"Imagenes de galería")
        ordering = ('order',)
        unique_together = ('entry','order',)
    
    
    
    
    
    
