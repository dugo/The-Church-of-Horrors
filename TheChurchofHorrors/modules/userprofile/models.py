# coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from filebrowser.fields import FileBrowseField
from django.utils.translation import ugettext as _

class Rol(models.Model):
    name = models.CharField(_('Rol'),max_length=100,unique=True,blank=False)
    sort = models.PositiveIntegerField(_('Orden'),help_text=_(u'Orden en el que se mostrará en la página de staffs'),unique=True,blank=False)
    
    def __unicode__(self):
        return unicode(self.name)
    
    class Meta:
        verbose_name = _('rol')
        verbose_name_plural = _('roles')
        ordering = ('sort',)

class UserProfile(models.Model):
    user = models.ForeignKey(User, verbose_name=_("Usuario"), unique=True,blank=False)
    description = models.CharField(_(u'Descripción'),max_length=160, help_text = _(u'Cómo te describes en 160 caracteres (un sms)'))
    rol = models.ForeignKey(Rol,verbose_name=_(u'Rol'), help_text=_(u'¿Qué papel desempeñas?'),blank=False,null=False)
    avatar = models.ImageField(blank=False,upload_to='avatars/',help_text=_(u'Tu avatar. Será redimensionado y convertido a blanco y negro'))
    #avatar = models.ImageField(blank=False,upload_to='avatars/')
    
    def get_items(self):
        return self.items.order_by('id')[:]
    
    def __unicode__(self):
        return unicode(self.user)
    
    def save(self,*args,**kwargs):
        
            super(type(self),self).save(*args,**kwargs)
            
            from PIL import Image
            import os

            im = Image.open(self.avatar.path)
            
            # resize process
            if im.size[0] <> 104:
                im = im.resize((104,int((float(im.size[1])/float(im.size[0]))*104.0),),Image.ANTIALIAS)
            
            # bw    
            im = im.convert('L')
                    
            im.save( self.avatar.path, "PNG")
            
            newname = "%s.png" % self.user.username
            
            os.rename(self.avatar.path, os.path.join(os.path.dirname(self.avatar.path),newname) )
            
            self.avatar.name = "avatars/%s" % newname
            
            print self.avatar.url
            
            super(type(self),self).save(*args,**kwargs)
            
    
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
    
