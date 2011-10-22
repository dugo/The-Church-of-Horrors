# coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from filebrowser.fields import FileBrowseField
from django.utils.translation import ugettext as _
     
class UserProfile(models.Model):
    user = models.ForeignKey(User, verbose_name=_("Usuario"), unique=True,blank=False)
    description = models.TextField(_(u'Descripción'))
    rol = models.CharField(_(u'Rol'),max_length=100)
    avatar = FileBrowseField(blank=False,directory='avatars/',extensions=[".jpg",".png",".jpeg",".gif"])
    #avatar = models.ImageField(blank=False,upload_to='avatars/')
    
    def get_items(self):
        return self.items.order_by('id')[:]
    
    def __unicode__(self):
        return unicode(self.user)
    
    class Meta:
        verbose_name = _('perfil de usuario')
        verbose_name_plural = _('perfiles de usuario')
        ordering = ('user',)
        

class UserProfileItem(models.Model):
    profile = models.ForeignKey(UserProfile, verbose_name=_("Perfil"),related_name="items")
    display_name = models.CharField(_(u'Nombre para mostrar'),max_length=20,blank=False)
    url = models.URLField(blank=False)
    
    def __unicode__(self):
        return unicode(self.display_name)

    class Meta:
        ordering = ('display_name',)
    
