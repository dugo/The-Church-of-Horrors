# coding=utf-8

import models

from django.contrib import admin
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from tinymce.widgets import TinyMCE
from django import forms
from django.utils.translation import ugettext as _

class Section(admin.ModelAdmin):
    model = models.Section
    
    readonly_fields = ('slug',)

class Subsection(admin.ModelAdmin):
    model = models.Subsection
    
    readonly_fields = ('slug',)

class ImageGalleryFormset(BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data and form.cleaned_data['main']:
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count <> 1:
            raise forms.ValidationError(_("Debes subir al menos una imagen y sólo debe haber una principal"))

class ImageGallery(admin.TabularInline):
    model = models.ImageGallery
    can_delete = True
    extra = 1
    
    formset = ImageGalleryFormset
    

class EntryForm(ModelForm):
    
    content = forms.CharField(label=_(u"Contenido"),widget=TinyMCE(attrs={'cols': 120, 'rows': 40}))
    
    class Meta:
        model = models.Entry

class Entry(admin.ModelAdmin):
    model = models.Entry
    form = EntryForm
    
    inlines = (ImageGallery,)
    
    list_display = ('__unicode__','gallery',)
    
    readonly_fields = ('slug',)
    
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.readonly_fields = ('slug',)
        else:
            self.readonly_fields = ('slug','author',) 
        return super(Entry, self).get_form(request, obj=None, **kwargs)
    
    
    def save_model(self, request, obj, form, change):
		if not hasattr(obj,'author'):
			obj.author = request.user
		obj.save()



admin.site.register(models.Section,Section)
admin.site.register(models.Subsection,Subsection)
admin.site.register(models.Entry,Entry)
