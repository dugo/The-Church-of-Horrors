# coding=utf-8

import models

from django.contrib import admin
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from django import forms
from django.utils.translation import ugettext as _

class Section(admin.ModelAdmin):
    model = models.Section

class Subsection(admin.ModelAdmin):
    model = models.Subsection

class ImageGallery(admin.TabularInline):
    model = models.ImageGallery
    can_delete = True
    extra = 1
    

class EntryForm(ModelForm):
    
    content = forms.CharField(label=_(u"Contenido"),widget=TinyMCE(attrs={'cols': 120, 'rows': 40}))
    
    class Meta:
        model = models.Entry

class Entry(admin.ModelAdmin):
    model = models.Entry
    form = EntryForm
    
    inlines = (ImageGallery,)
    
    readonly_fields = ('slug',)



admin.site.register(models.Section,Subsection)
admin.site.register(models.Subsection,Subsection)
admin.site.register(models.Entry,Entry)
