# coding=utf-8

import models

from django.contrib import admin
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from tinymce.widgets import TinyMCE
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
import re
import os.path

class NumberForm(ModelForm):

    def clean_published(self):
        if self.cleaned_data.get("published"):
            if not self.instance.pk:
                return False

            if not self.instance.entries.filter(is_editorial=True).count():
                raise forms.ValidationError(u"Imposible publicar. Debe marcar una entrada cómo Editorial")

            if not self.instance.entries.filter(is_cartoon=True).count():
                raise forms.ValidationError(u"Imposible publicar. Debe marcar una entrada cómo Viñeta")


        return self.cleaned_data.get("published")
    
    """def clean(self):
        if self.cleaned_data.get("published") and self.instance:
            raise forms.ValidationError(u"Antes de publicar debe añadir)


        return self.cleaned_data"""
    
    class Meta:
        model = models.Number

class Number(admin.ModelAdmin):
    list_display = ("__unicode__","month","year","published")
    model = models.Number
    form = NumberForm
    

class SubsectionTag(admin.TabularInline):
    model = models.SubsectionTag
    can_delete = True
    extra = 0

class Subsection(admin.ModelAdmin):
    model = models.Subsection
    
    readonly_fields = ('slug',)
    list_display = ('name','sort',)
    inlines = (SubsectionTag,)

class ImageGalleryFormset(BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        count = 0
        total = 0
        orders = []
        for form in self.forms:
            try:
                if form.cleaned_data and not form.cleaned_data['DELETE']:
                    relpath = re.sub(r'^%s' % settings.MEDIA_URL, "", form.cleaned_data['file'])
                    
                    if not os.path.exists(os.path.join(settings.MEDIA_ROOT,relpath)):
                        raise forms.ValidationError(_(u"El fichero '%s' no existe" % form.cleaned_data['file']))
                
                if form.cleaned_data and not form.cleaned_data['DELETE']:
                    
                    if form.cleaned_data['order'] in orders:
                        raise forms.ValidationError(_(u"Aseguresé de que los órdenes de las imágenes no se repiten"))
                    
                    orders.append( form.cleaned_data['order'] )
                    
                    total+=1
                
                if form.cleaned_data and not form.cleaned_data['DELETE'] and form.cleaned_data['main']:
                    count += 1
                
                
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count <> 1:
            raise forms.ValidationError(_(u"Debes subir al menos una imagen y sólo debe haber una marcada como principal"))
        
        """if self.instance.show_gallery and total <= 1:
            raise forms.ValidationError(_(u"Para que aparezca la galería debes de subir una imagen o más"))"""

class ImageGallery(admin.TabularInline):
    model = models.ImageGallery
    can_delete = True
    extra = 1
    
    formset = ImageGalleryFormset

class CounterAdmin(admin.ModelAdmin):
    counted_fields = ()
    
    #really for textareas
    max_lengths = {'abstract': 400,'brief':450}
    
    class Media:
        js = ('%sthechurch/js/jquery-1.6.4.min.js' % settings.STATIC_URL,
            '%sthechurch/js/jquery.charCount.js' % settings.STATIC_URL,)
        
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super(CounterAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in self.counted_fields:
            field.widget.attrs['mymaxlength'] = self.max_lengths[db_field.name]
            field.widget.attrs['class'] = 'counted ' + field.widget.attrs.get('class','')
        return field        

class EntryForm(ModelForm):
    
    content = forms.CharField(label=_(u"Contenido"),widget=TinyMCE(attrs={'cols': 120, 'rows': 40}))
    brief = forms.CharField(label=_(u'Resumen'),widget=forms.Textarea(attrs={'class':'counted','mymaxlength':'450'}),help_text = _(u'Un breve resumen representativo de la entrada. Si queda vacío se cogerá el primer párrafo.'),required=False)
    
    def clean_is_editorial(self):
        if self.cleaned_data.get("is_editorial") and self.cleaned_data.get("number"):
            editorial = self.cleaned_data.get("number").editorial
            if not editorial is None and editorial.id <> self.instance.id :
                raise forms.ValidationError(u'Este Número ya tiene un artículo marcado cómo editorial, desmárquelo para continuar.')

        return self.cleaned_data.get("is_editorial")

    def clean_is_cartoon(self):
        if self.cleaned_data.get("is_cartoon") and self.cleaned_data.get("number"):
            cartoon = self.cleaned_data.get("number").cartoon
            if not cartoon is None and cartoon.id <> self.instance.id :
                raise forms.ValidationError(u'Este Número ya tiene un artículo marcado cómo viñeta, desmárquelo para continuar.')

        return self.cleaned_data.get("is_cartoon")

    class Meta:
        model = models.Entry

class CommentInline(admin.TabularInline):
    model = models.Comment
    can_delete = True
    extra = 0
    readonly_fields = ('author','email','content','time','website')


class Comment(admin.ModelAdmin):

    list_display = ('author','content','email','website','time',)
    
    ordering = ('-time',)




class Entry(CounterAdmin):
    model = models.Entry
    form = EntryForm
    
    inlines = (CommentInline,)

    search_fields = ('title',)
    
    list_display = ('__unicode__','author','created','published','views','ncomments','view',)

    list_filter = ('number',)
    
    readonly_fields = ('slug',)
    
    date_hierarchy = 'created'

    exclude = ('views','ncomments')
    
    def get_form(self, request, obj=None, **kwargs):
        
        form = super(Entry, self).get_form(request, obj=None, **kwargs)
        
        if form.base_fields.has_key('author'):
            form.base_fields['author'].initial = request.user
        
        if not request.user.is_superuser and not request.user.get_profile().is_editor:
            self.readonly_fields = ('slug',)
            self.exclude = ('author','published','is_editorial','is_cartoon','number','views','ncomments')
            #form.base_fields['author'].queryset = form.base_fields['author'].queryset.filter(id=request.user.id)
            
        return form
    
    def has_delete_permission(self, request, obj=None):
        
        if obj is None:
            return True
        
        if not request.user.is_superuser and not request.user.get_profile().is_editor and (obj.author_id <> request.user.id or obj.published ):
            return False
        
        return True
    
    def save_model(self, request, obj, form, change):
        
        if not hasattr(obj,'author') or obj.author is None or (not request.user.is_superuser and not request.user.get_profile().is_editor):
            obj.author = request.user
        
        obj.save()
    
    def view(self,o):
        return "<a href='%s' onclick='window.open(this.href);return false;'>%s</a>" % (o.get_absolute_url(),_(u'Ver'))
    view.allow_tags = True
    view.short_description = _(u'Ver')
    
    """
    def save_formset(self, request, form, formset, change): 
        import os.path
        instances = formset.save(commit=False)
        for i in instances:
            if os.path.exists(os.path.join(settings.MEDIA_ROOT, i.file.path)):
                i.save()
        #formset.save()"""
    
    def queryset(self, request):
        qs = super(Entry, self).queryset(request)

        if not request.user.is_superuser and not request.user.get_profile().is_editor:
            return qs.filter(author__id=request.user.id)
        
        return qs

admin.site.register(models.Number,Number)
admin.site.register(models.Subsection,Subsection)
admin.site.register(models.Entry,Entry)
admin.site.register(models.Comment,Comment)
