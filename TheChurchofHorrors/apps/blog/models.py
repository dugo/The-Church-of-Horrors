# coding=utf-8

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from tinymce import models as tinymce_models


class Section(models.Model):
    name = models.CharField(_(u"Nombre"),max_length=255,unique=True,db_index=True,blank=False)
    
    class Meta:
        verbose_name = _(u"sección")
        verbose_name_plural = _(u"secciones")
        ordering = ('name',)

    def save(self,*args,**kwargs):
        if self.name:
            self.name = self.name.upper()
        super(type(self),self).save(*args,**kwargs)

class Subsection(models.Model):
    name = models.CharField(_(u"Nombre"),max_length=255,unique=True,db_index=True,blank=False)

    class Meta:
        verbose_name = _(u"subsección")
        verbose_name_plural = _(u"subsecciones")
        ordering = ('name',)


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
    
    class Meta:
        verbose_name = _(u"entrada")
        ordering = ('-created',)

class ImageGallery(models.Model):
    entry = models.ForeignKey(Entry,verbose_name=_(u"Entrada"),related_name="images")
    file = models.ImageField(blank=False,upload_to='images/%Y/%m')
    order = models.PositiveIntegerField(_(u'Orden'))
    
    class Meta:
        verbose_name = _(u"Imagen de galería")
        verbose_name_plural = _(u"Imagenes de galería")
        ordering = ('order',)
        unique_together = ('entry','order',)
    
    
    
    
    
    
