# coding=utf-8

import models

from django.contrib import admin
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site


class UserProfileForm( forms.ModelForm ):
    description = forms.CharField(label=_(u'Descripción'),widget=forms.Textarea(attrs={'class':'counted','maxlength':'160'}),help_text = _(u'¿Cómo te describirías en un sms (160 caracteres)?') )
    
    class Meta:
        model = models.UserProfile

class Rol(admin.ModelAdmin):
    model = models.UserProfile
    
    list_display = ('__unicode__','sort',)

class CounterAdmin(admin.ModelAdmin):
    counted_fields = ()
    
    #really for textareas
    max_lengths = {'abstract': 400,'description':160}
    
    class Media:
        js = ('%sthechurch/js/jquery-1.6.4.min.js' % settings.STATIC_URL,
            '%sthechurch/js/jquery.charCount.js' % settings.STATIC_URL,)
        
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(CounterAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in self.counted_fields:
            field.widget.attrs['maxlength'] = self.max_lengths[db_field.name]
            field.widget.attrs['class'] = 'counted ' + field.widget.attrs.get('class','')
        return field    

class UserProfileItem(admin.TabularInline):
    model = models.UserProfileItem
    can_delete = True
    extra = 1

class UserProfile(CounterAdmin):
    
    form = UserProfileForm
    
    model = models.UserProfile
    
    list_display = ('user','get_avatar','url')
    
    inlines = (UserProfileItem,)
    
    counted_fields = ('description',)
    
    def get_avatar(self,obj):
        return "<img src='%s' height=50 width=auto/>" % unicode(obj.avatar.url)
    get_avatar.allow_tags = True
    get_avatar.short_description = "Avatar"
    
    def url(self,obj):
        return u"<a href='%s' target='_blank'/>%s%s</a>" % (obj.get_absolute_url(),Site.objects.get_current().domain,obj.get_absolute_url())
    url.allow_tags = True
    url.short_description = _("En el sitio")

    def queryset(self, request):
        qs = super(UserProfile, self).queryset(request)

        if not request.user.is_superuser:
            return qs.filter(user__id=request.user.id)
        
        return qs
    
    def save_model(self, request, obj, form, change):
        
        if not request.user.is_superuser:
            obj.user = request.user
                   
        super(UserProfile,self).save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        
        
        
        if not request.user.is_superuser:
            self.exclude = ('user',)
            form = super(UserProfile, self).get_form(request, obj=None, **kwargs)
            #self.exclude = ('user',)
            form.base_fields['rol'].queryset = form.base_fields['rol'].queryset.filter(name="Redactor")
            form.base_fields['rol'].initial = form.base_fields['rol'].queryset[:1].get()
        else:
            
            form = super(UserProfile, self).get_form(request, obj=None, **kwargs)
            form.base_fields['user'].initial = request.user
        
        form.base_fields['name'].initial = request.user.get_full_name() if request.user.get_full_name() else unicode(request.user)    
        
        return form



admin.site.register(models.UserProfile,UserProfile)
admin.site.register(models.Rol,Rol)
