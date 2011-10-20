# coding=utf-8

import models

from django.contrib import admin
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from tinymce.widgets import TinyMCE
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings

class Section(admin.ModelAdmin):
    model = models.Section
    
    readonly_fields = ('slug',)

class Subsection(admin.ModelAdmin):
    model = models.Subsection
    
    readonly_fields = ('slug',)
    list_display = ('name','sort',)

class ImageGalleryFormset(BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        total = 0
        for form in self.forms:
            try:
                if form.cleaned_data and not form.cleaned_data['DELETE']:
                    total+=1
                
                if form.cleaned_data and not form.cleaned_data['DELETE'] and form.cleaned_data['main']:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count <> 1:
            raise forms.ValidationError(_(u"Debes subir al menos una imagen y sólo debe haber una marcada como principal"))
        
        if self.instance.show_gallery and total <= 1:
            raise forms.ValidationError(_(u"Para que aparezca la galería debes de subir una imagen o más"))

class ImageGallery(admin.TabularInline):
    model = models.ImageGallery
    can_delete = True
    extra = 1
    
    formset = ImageGalleryFormset
    

class EntryForm(ModelForm):
    
    content = forms.CharField(label=_(u"Contenido"),widget=TinyMCE(attrs={'cols': 120, 'rows': 40},  mce_attrs = { "style_formats" : [ {"title" : _('Cita'), "block" : 'blockquote'} ], "content_css": "%sthechurch/css/editor.css" % settings.STATIC_URL }))
    
    class Meta:
        model = models.Entry

class Entry(admin.ModelAdmin):
    model = models.Entry
    form = EntryForm
    
    inlines = (ImageGallery,)
    
    list_display = ('__unicode__','author','published','gallery','view',)
    
    readonly_fields = ('slug',)
    
    def get_form(self, request, obj=None, **kwargs):
        
        form = super(Entry, self).get_form(request, obj=None, **kwargs)
        
        if form.base_fields.has_key('author'):
            form.base_fields['author'].initial = request.user
        
        if not request.user.is_superuser:
            self.exclude = ('author','gallery','published',)
            #form.base_fields['author'].queryset = form.base_fields['author'].queryset.filter(id=request.user.id)
            
        return form
    
    
    def save_model(self, request, obj, form, change):
        
        if hasattr(obj,'author') and not request.user.is_superuser and request.user.id <> obj.author.id:
            return
        
        if not hasattr(obj,'author') or not request.user.is_superuser:
            obj.author = request.user
                   
        obj.save()
    
    def view(self,o):
        return "<a href='%s' onclick='window.open(this.href);return false;'>%s</a>" % (o.get_absolute_url(),_(u'Ver'))
    view.allow_tags = True
    view.short_description = _(u'Ver')
    
    def queryset(self, request):
        qs = super(Entry, self).queryset(request)

        if not request.user.is_superuser:
            return qs.filter(author__id=request.user.id)
        
        return qs




admin.site.register(models.Section,Section)
admin.site.register(models.Subsection,Subsection)
admin.site.register(models.Entry,Entry)
