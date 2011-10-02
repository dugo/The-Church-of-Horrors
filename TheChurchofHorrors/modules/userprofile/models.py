# coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
     
class UserProfile(models.Model):
    user = models.ForeignKey(User, verbose_name=_("Usuario"), unique=True,blank=False)
    description = models.TextField(_(u'Descripción'))
    rol = models.CharField(_(u'Rol'),max_length=100)
    
    class Meta:
        verbose_name = _('perfil de usuario')
        verbose_name_plural = _('perfiles de usuario')
        ordering = ('user',)
        

class UserProfileItem(models.Model):
    profile = models.ForeignKey(UserProfile, verbose_name=_("Perfil"),related_name="items")
    display_name = models.CharField(_(u'Nombre para mostrar'),max_length=20,blank=False)
    url = models.URLField(blank=False)

    class Meta:
        ordering = ('display_name',)
    
