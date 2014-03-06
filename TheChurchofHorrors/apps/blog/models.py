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
from django.core.cache import cache
from dateutil.relativedelta import relativedelta
import datetime,sys,random

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^tinymce\.models\.HTMLField"])

def in_sync():
    return False
    return "syncdb" in sys.argv or "migrate" in sys.argv

"""class Section(models.Model):
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
        super(type(self),self).save(*args,**kwargs)"""

MONTH_CHOICES = ( (1,'Enero',),
                (2,'Febrero'),
                (3,'Marzo'),
                (4,'Abril'),
                (5,'Mayo'),
                (6,'Junio'),
                (7,'Julio'),
                (8,'Agosto'),
                (9,'Septiembre'),
                (10,'Octubre'),
                (11,'Noviembre'),
                (12,'Diciembre'),
    )

class Number(models.Model):
    number = models.PositiveIntegerField(u"Número",unique=True,db_index=True)
    month = models.PositiveIntegerField(u"Mes",choices=MONTH_CHOICES)
    year = models.PositiveIntegerField(u"Año")
    imagen = FileBrowseField(blank=False,format='image',extensions=[".jpg",".png",".jpeg",".gif"],default='')
    published = models.BooleanField("Publicado",default=False,)

    @property
    def modified(self):
        return self.entries.all().order_by("-modified").values('modified')[0]['modified']

    @property
    def editorial(self):
        try:
            return self.entries.get(is_editorial=True)
        except Entry.DoesNotExist:
            return None

    @property
    def cartoon(self):
        try:
            return self.entries.get(is_cartoon=True)
        except Entry.DoesNotExist:
            return None

    @models.permalink
    def get_absolute_url(self):
        return ('number', (), {'number': self.number,'month':self.month,'year':self.year})

    @property
    def other_entries(self):
        return self.entries.filter(is_editorial=False,is_cartoon=False,published=True)

    @property
    def other_entries_random(self):
        return self.other_entries.order_by("?")

    @property
    def all_entries(self):
        return self.entries.filter(published=True)

    @classmethod
    def get_current(cls):
        return cls.objects.filter(published=True).order_by("-number")[0]

    def is_current(self):
        return Number.objects.filter(published=True).values("id").order_by("-number")[0]['id'] == self.id

    @classmethod
    def get_anteriores(cls):
        if settings.DEBUG:
            return [cls.get_current(),cls.get_current(),cls.get_current(),cls.get_current(),cls.get_current()]
        else:
            return cls.objects.filter(published=True).order_by("-number")[1:]

    def get_more_comment(self):
        return self.other_entries.filter(published=True).order_by("-ncomments")

    def get_more_view(self):
        return self.other_entries.filter(published=True).order_by("-views")

    def get_more_shared(self):
        return self.other_entries.filter(published=True).order_by("-shared")

    def __unicode__(self):
        return u"Número %d"%self.number

    def get_sitios(self):
        qs = UserProfile.objects.filter(rols__rol__id=2,user__entries__id__in=self.entries.filter(published=True,is_cartoon=False,).values_list("id",flat=True))
        qs = list(set(qs))
        random.shuffle(qs)

        return qs

    def get_sitios(self):
        qs = UserProfile.objects.filter(rols__rol__id=2,user__entries__id__in=Entry.objects.filter(published=True,number__published=True,is_cartoon=False,).values_list("id",flat=True))
        qs = list(set(qs))
        random.shuffle(qs)

        return qs

    @classmethod
    def get_published(cls):
        return cls.objects.filter(published=True)

    def get_subsections(self):

        return Subsection.objects.filter(id__in=self.other_entries.values_list("subsection",flat=True))

    class Meta:
        ordering = ("-number",)
        verbose_name = "Número"


class Subsection(models.Model):
    name = models.CharField(_(u"Nombre"),max_length=255,unique=True,db_index=True,blank=False)
    slug = models.SlugField(max_length=255,unique=True,blank=True,help_text=u"Será generada automaticamente a partir del nombre")
    sort = models.PositiveIntegerField(_(u"Orden"),default=0,blank=False,null=False,help_text=_(u"En el que se mostrará en el menú"))
    color = models.CharField("Color Css",max_length="7",help_text="#3f3f3f",default="")
    hidden = models.BooleanField("Oculta",default=False)
    
    def __unicode__(self):
        return unicode(self.name)

    @property
    def other_entries(self):
        return self.entries.filter(published=True,number__published=True)

    @property
    def other_entries_random(self):
        return self.other_entries.order_by("?")

    class Meta:
        verbose_name = _(u"categoría")
        verbose_name_plural = _(u"categorías")
        ordering = ('sort',)

    @models.permalink
    def get_absolute_url(self):
        return ('subsection', (), {
            'slug': self.slug})
    
    @classmethod
    def get_css_colors(cls):
        css = """
        .home .short-entry.%(slug)s { border-bottom: 3px solid %(color)s }
        .entry .content-entry.%(slug)s .link { color: %(color)s }
        #header #subsections.%(slug)s {border-top:3px solid %(color)s}
        .cartoon .%(slug)s .cartoon-title {border-bottom:3px solid %(color)s}
        """
        ret = ""

        for ss in cls.objects.exclude(color=""):
            ret+=css%dict(color=ss.color,slug=ss.slug)

        return ret


    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(type(self),self).save(*args,**kwargs)

class SubsectionTag(models.Model):
    tag = models.ForeignKey("taggit.tag",verbose_name=_(u"Etiqueta"))
    subsection = models.ForeignKey(Subsection,verbose_name=_(u"Categoría"),related_name="tags")
    sort = models.PositiveIntegerField(_(u"Orden"),default=0,blank=False,null=False,help_text=_(u"En el que se mostrará en el menú"))

    def __unicode__(self):
        return unicode(self.tag)

    class Meta:
        verbose_name = _(u"etiqueta de categoría")
        verbose_name_plural = _(u"etiquetas de categoría")
        ordering = ('sort',)
        unique_together = ( ('subsection','tag',) ,('sort','subsection',))
    
    @models.permalink
    def get_absolute_url(self):
        
        return ('subsection_tag', (), {
            'subsection': self.subsection.slug,
            'tag': self.tag.slug})

class Entry(models.Model):
    title = models.CharField(_(u"Título"),max_length=255,blank=False,unique=True)
    content = tinymce_models.HTMLField(_("Contenido"),blank=False,)
    brief =  models.CharField(_(u'Resumen'),max_length=450, help_text = _(u'Un breve resumen representativo de la entrada. Si queda vacío se cogerá el primer párrafo.'),blank=True)
    author = models.ForeignKey(User,verbose_name=_(u"Autor"),related_name="entries",blank=False,null=True)
    ilustrator = models.ForeignKey(User,verbose_name=_(u"Ilustrador"),related_name="ilustrations",blank=True,null=True,default=None)
    number = models.ForeignKey(Number,verbose_name=_(u"Número"),null=True,default=None,blank=True,related_name='entries')
    #section = models.ForeignKey(Section,verbose_name=_(u"Sección"))
    subsection = models.ForeignKey(Subsection,verbose_name=_(u"Categoría"),related_name="entries")
    created = models.DateTimeField(_(u'Creado'),help_text=_("La hora no tiene importancia"))
    modified = models.DateTimeField(_(u'Modificado'),auto_now=True)
    published = models.BooleanField(_(u'Publicado'),default=False,blank=False)
    slug = models.SlugField(max_length=255,unique=True,blank=True,help_text=_(u"Será generada automaticamente a partir del título"))
    views = models.PositiveIntegerField("V",db_index=True,default=0,blank=True)
    ncomments = models.PositiveIntegerField("C",db_index=True,default=0,blank=True)
    shared = models.PositiveIntegerField("S",db_index=True,default=0,blank=True)
    #gallery = models.BooleanField(_(u'Mostrar en galería de HOME'),help_text=_(u'Se mostrará sólo la imagen marcada cómo principal'),default=False,blank=True)
    #show_gallery = models.BooleanField(_(u'Mostrar galería en entrada'),help_text=_(u'Se mostrará en la propia entrada una galería con las imágenes en el orden establecido. Si hay sólo una imagen se mostrará la imagen estática'),default=False,blank=True)
    tags = TaggableManager()
    imagen = FileBrowseField(blank=False,format='image',extensions=[".jpg",".png",".jpeg",".gif"],default='')
    is_editorial = models.BooleanField(_(u'Es editorial'),default=False,blank=True)
    is_cartoon = models.BooleanField(_(u'Es viñeta'),default=False,blank=True)
    
    def __unicode__(self):
        return unicode(self.title)
    
    def add_view_mark(self,ip,user):
        if not self.published:
            return 

        key = "thechurch-view-%s-%s"%(ip,user.id,)
        if not cache.get(key) and not self.author==user:
            self.views+=1
            self.save()

        cache.set(key,"ok",3600)


    @classmethod
    def get_archive(self,year,month):
        current = datetime.date(int(year),int(month),1)
        return self.objects.filter(created__gte=current,created__lt=current+relativedelta(months=1))

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
        
        
        
        return self.objects.filter(id__in=[h.fields()['id'] for h in hits]).filter(published=True)
    
    @classmethod
    def get_home_gallery(self):
        return Entry.objects.filter(published=True,gallery=True).order_by('-created')

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(type(self),self).save(*args,**kwargs)

    class Meta:
        verbose_name = _(u"entrada")
        ordering = ('-created',)

    @models.permalink
    def get_absolute_url(self):
        return ('entry', (), {
            'number':self.number.number,
            'month':self.number.month,
            'year':self.number.year,
            'subsection': self.subsection.slug,
            'slug': self.slug})
    
    
    """@models.permalink
    def get_absolute_url(self):
        return ('common', (), {
            'slug': self.slug})"""
    
    def get_admin_url(self):
        return reverse("admin:blog_entry_change", args=[self.id])
    
    def get_approved_comments(self):
        return self.comments.filter(approved=True)
    
    def get_comments(self):
        return self.comments.all()

    def get_related(self):
        return Entry.objects.filter(subsection__hidden=False,number__published=True,tags__name__in=self.tags.values_list("name",flat=True).all()[:]).exclude(id=self.id).exclude(published=False).distinct()[:4]
    
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

        if author.get_profile().is_ilustrator:
            entries = Entry.objects.filter(published=True,ilustrator__id=author.id,number__published=True).order_by('-created')
        else:
            entries = Entry.objects.filter(published=True,author__id=author.id,is_cartoon=False,number__published=True).order_by('-created')
            
            
        if entry:
            return entries.exclude(id=entry.id)
        
        return entries
    
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
        if self.imagen:
            return self.imagen
        return self.images.get(main=True).file
    
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
        #unique_together = ('entry','order',)
    

class Comment(models.Model):
    entry = models.ForeignKey(Entry,verbose_name=_(u"Entrada"),related_name="comments",blank=True)
    author = models.CharField(_(u'Nombre'),max_length=256)
    email = models.EmailField(_(u'Email'),max_length=256)
    time = models.DateTimeField(_(u'Enviado'),auto_now_add=False)
    website = models.URLField(_(u'Web'),blank=True,default="")
    approved = models.BooleanField(_(u'Aprobado'),blank=True,default=True)
    content = models.TextField()

    def save(self,*args,**kwargs):

        if not getattr(self,"pk",None):
            e = self.entry
            e.ncomments+=1
            e.save()

        super(Comment,self).save(self,*args,**kwargs)

    
    def notify(self):
        to = set(UserProfile.get_by_rol(settings.BLOG_EDITOR_ROL_ID).values_list("user__email",flat=True))
        to.add(self.entry.author.email)
        [ to.add(e[1]) for e in settings.ADMINS ]
        [ to.add(e) for e in Comment.objects.filter(entry=self.entry).values_list("email",flat=True) ]
        
        
        msg = "Se ha añadido un nuevo comentario a la entrada '%s'.\n\nPuedes verlo en http://thechurchofhorrors.com%s#comments" % (self.entry,self.entry.get_absolute_url())

        for e in to:
            if e:
                send_mail('[TheChurchofHorrors] Nuevo comentario', msg, settings.BLOG_DEFAULT_SENDER, [e], fail_silently=False)
    
    def __unicode__(self):
        return self.content
    
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

    try:
        writer = ix.writer()
    except:
        return
    
    tags = []
    for t in instance.tags.all():
        try:
            tags.append(unicode(t.name))
        except:
            pass
        
    tags = u','.join(tags)

    try:
    
        if created:
            writer.add_document(title=instance.title, content=instance.content,tags=tags,author=instance.author.get_profile().name+u"\n"+instance.author.username,
                                        id=unicode(instance.pk))
            writer.commit()
        else:
            writer.update_document(title=instance.title, content=instance.content,tags=tags,author=instance.author.get_profile().name+u"\n"+instance.author.username,
                                        id=unicode(instance.pk))
            writer.commit()
    except:
        pass

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
        
                
    
