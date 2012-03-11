# coding=utf-8

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from django.template.defaultfilters import slugify
from django.conf import settings
from filebrowser.fields import FileBrowseField
from taggit.managers import TaggableManager
from django.core.urlresolvers import reverse


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
    sort = models.PositiveIntegerField(_(u"Orden"),default=0,blank=False,null=False,help_text=_(u"En el que se mostrará en el menú"))
    
    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = _(u"categoría")
        verbose_name_plural = _(u"categorías")
        ordering = ('sort',)

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
    brief =  models.CharField(_(u'Resumen'),max_length=450, help_text = _(u'Un breve resumen representativo de la entrada. Si queda vacío se cogerá el primer párrafo.'),blank=True)
    author = models.ForeignKey(User,verbose_name=_(u"Autor"),related_name="entries",blank=True,null=True)
    section = models.ForeignKey(Section,verbose_name=_(u"Sección"))
    subsection = models.ForeignKey(Subsection,verbose_name=_(u"Categoría"))
    created = models.DateTimeField(_(u'Creado'),help_text=_("La hora no tiene importancia"))
    modified = models.DateTimeField(_(u'Modificado'),auto_now=True)
    published = models.BooleanField(_(u'Publicado'),default=False,blank=False)
    slug = models.SlugField(max_length=255,unique=True,blank=True,help_text=_(u"Será generada automaticamente a partir del título"))
    gallery = models.BooleanField(_(u'Mostrar en galería de HOME'),help_text=_(u'Se mostrará sólo la imagen marcada cómo principal'),default=False,blank=True)
    show_gallery = models.BooleanField(_(u'Mostrar galería en entrada'),help_text=_(u'Se mostrará en la propia entrada una galería con las imágenes en el orden establecido. Si hay sólo una imagen se mostrará la imagen estática'),default=False,blank=True)
    tags = TaggableManager()
    
    def __unicode__(self):
        return unicode(self.title)
    
    """@classmethod
    def search(self,q):
        return self.objects.raw("SELECT * FROM blog_entry WHERE MATCH (title) AGAINST ('%s');" % q)"""
        
    @classmethod
    def search(self,q):
        from whoosh.filedb.filestore import FileStorage
        from whoosh.qparser import MultifieldParser
        storage = FileStorage(settings.WHOOSH_INDEX)
        ix = storage.open_index()
        q = q.replace('+', ' AND ').replace(' -', ' NOT ')
        parser = MultifieldParser(["content","title","tags","author"], schema=ix.schema)
        qry = parser.parse(q)
        searcher = ix.searcher()
        hits = searcher.search(qry)
        
        
        
        return self.objects.filter(id__in=[h.fields()['id'] for h in hits])
    
    @classmethod
    def get_home_gallery(self):
        return Entry.objects.filter(published=True,gallery=True).order_by('-created')

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
    
    def get_admin_url(self):
        return reverse("admin:blog_entry_change", args=[self.id])
    
    def get_approved_comments(self):
        return self.comments.filter(approved=True)
    
    def get_comments(self):
        return self.comments.all()
        
    
    def n_comments(self):
        return self.comments.all().count()
    
    @classmethod
    def get_last(self,**kwargs):
        
        if kwargs:
            return Entry.objects.order_by('-created').filter(**kwargs).filter(published=True)
        else:
            return Entry.objects.order_by('-created').filter(published=True)
        
    @classmethod
    def get_last_by_author(self,author,entry=None,max=settings.BLOG_OTHER_LAST_ENTRIES):

        entries = Entry.objects.filter(published=True,author__id=author.id).order_by('-created')
        
        if entry:
            return entries.exclude(id=entry.id)
        
        return entries[:max]
    
    @classmethod    
    def get_last_by_section(self,section=None,max=settings.BLOG_RIGHT_LAST_ENTRIES):
        
        entries = {}
        
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
        return self.images.get(main=True)
    
    def get_brief(self):
        import re
        from templatetags.blog import unescape
        
        if self.brief:
            return unescape(re.sub(r'<[^>]+>','',self.brief))

        content = unescape(re.sub(r'<[^>]+>','',self.content))
        
        if len(content) < 300:
            return content
        
        idx = 0
        for i in range(300,450):
            if content[i] == ".":
                idx = i
                break
        else:
            return content[:450]+"..."
        
        return content[:idx+1]
    
class ImageGallery(models.Model):
    entry = models.ForeignKey(Entry,verbose_name=_(u"Entrada"),related_name="images")
    file = FileBrowseField(blank=False,format='image',extensions=[".jpg",".png",".jpeg",".gif"])
    #file = models.ImageField(blank=False,upload_to='images/%Y/%m')
    order = models.PositiveIntegerField(_(u'Orden en la galería'),default=1)
    main = models.BooleanField(_(u'Usar como principal'))
    adjust = models.BooleanField(_(u'Auto-ajustar'),default=False)
    
    def __unicode__(self):
		return unicode(self.file)
    
    class Meta:
        verbose_name = _(u"Imagen de galería")
        verbose_name_plural = _(u"Imagenes de galería")
        ordering = ('order',)
        unique_together = ('entry','order',)
    

class Comment(models.Model):
    entry = models.ForeignKey(Entry,verbose_name=_(u"Entrada"),related_name="comments",blank=True)
    author = models.CharField(_(u'Nombre'),max_length=256)
    email = models.EmailField(_(u'Email'),max_length=256)
    time = models.DateTimeField(_(u'Enviado'),auto_now_add=False)
    website = models.URLField(_(u'Web'),blank=True,default="")
    approved = models.BooleanField(_(u'Aprobado'),blank=True,default=True)
    content = models.TextField()
    
    def notify(self):
        to = set(UserProfile.get_by_rol(settings.BLOG_EDITOR_ROL_ID).values_list("user__email",flat=True))
        to.add(self.entry.author.email)
        [ to.add(e[1]) for e in settings.ADMINS ]
        [ to.add(e) for e in Comment.objects.filter(entry=self.entry).values_list("email",flat=True) ]
        
        
        msg = "Se ha añadido un nuevo comentario a la entrada '%s'.\n\nPuedes verlo en http://thechurchofhorrors.com%s#comments" % (self.entry,self.entry.get_absolute_url())

        for e in to:
            if e:
                send_mail('[TheChurchofHorrors] Nueva comentario', msg, settings.BLOG_DEFAULT_SENDER, [e], fail_silently=False)
        
    
    class Meta:
        verbose_name = _(u"comentario")
        ordering = ('time',)


# notify to editors signal
from django.db.models.signals import post_save
from django.dispatch import receiver
from userprofile.models import UserProfile
from django.core.mail import send_mail
 
@receiver(post_save, sender=Entry)
def notify_editors(sender, instance, created, **kwargs):
    
    if created: 
        editors = list(UserProfile.get_by_rol(settings.BLOG_EDITOR_ROL_ID).values_list("user__email",flat=True))
        
        msg = "Se ha creado una nueva entrada.\nPuedes verla en http://thechurchofhorrors.com%s" % instance.get_admin_url()

        send_mail('[TheChurchofHorrors] Nueva entrada', msg, settings.BLOG_DEFAULT_SENDER, editors, fail_silently=False)


""" WHOOSH """

from django.db.models import signals
import os
from whoosh import fields
from whoosh.filedb.filestore import FileStorage

WHOOSH_SCHEMA = fields.Schema(title=fields.TEXT(stored=True),
                              content=fields.TEXT,
                              tags=fields.TEXT,
                              author=fields.TEXT,
                              id=fields.ID(stored=True, unique=True))

def create_index(sender=None, **kwargs):
    if not os.path.exists(settings.WHOOSH_INDEX):
        os.mkdir(settings.WHOOSH_INDEX)
        storage = FileStorage(settings.WHOOSH_INDEX)
        ix = storage.create_index(schema=WHOOSH_SCHEMA)

signals.post_syncdb.connect(create_index)


def update_index(sender, instance, created, **kwargs):
    storage = FileStorage(settings.WHOOSH_INDEX)
    ix = storage.open_index()
    writer = ix.writer()
    
    tags = []
    for t in instance.tags.all():
        try:
            tags.append(unicode(t.name))
        except:
            pass
        
    tags = u','.join(tags)
    
    if True:
        writer.add_document(title=instance.title, content=instance.content,tags=tags,author=instance.author.get_profile().name+u"\n"+instance.author.username,
                                    id=unicode(instance.pk))
        writer.commit()
    else:
        writer.update_document(title=instance.title, content=instance.content,tags=tags,author=instance.author.get_profile().name+u"\n"+instance.author.username,
                                    id=unicode(instance.pk))
        writer.commit()

signals.post_save.connect(update_index, sender=Entry)

""" END WHOOSH """

"""
@receiver(post_save, sender=Comment)
def notify_newcomment(sender, instance, created, **kwargs):
    
    if created: 
        to = set(UserProfile.get_by_rol(settings.BLOG_EDITOR_ROL_ID).values_list("user__email",flat=True))
        to.add(instance.entry.author.email)
        for e in settings.BLOG_CONTACT_EMAILS:
            to.add(e)
        
        
        msg = "Se ha añadido un nuevo comentario.\nPuedes verlo en http://thechurchofhorrors.com%s#comments" % instance.entry.get_absolute_url()

        send_mail('[TheChurchofHorrors] Nueva comentario', msg, settings.BLOG_DEFAULT_SENDER, to, fail_silently=False)"""
        
                
    
