# coding=utf-8

import models

from django.contrib import admin

class Rol(admin.ModelAdmin):
    model = models.UserProfile
    
    list_display = ('__unicode__','sort',)
    

class UserProfileItem(admin.TabularInline):
    model = models.UserProfileItem
    can_delete = True
    extra = 1

class UserProfile(admin.ModelAdmin):
    model = models.UserProfile
    
    list_display = ('user','get_avatar',)
    
    inlines = (UserProfileItem,)
    
    def get_avatar(self,obj):
        return "<img src='%s' height=50 width=auto/>" % unicode(obj.avatar)
    get_avatar.allow_tags = True
    get_avatar.short_description = "Avatar"

    def queryset(self, request):
        qs = super(UserProfile, self).queryset(request)

        if not request.user.is_superuser:
            return qs.filter(user__id=request.user.id)
        
        return qs
    
    def save_model(self, request, obj, form, change):
        
        if not request.user.is_superuser and request.user.id <> obj.user.id:
            return
        
        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        
        form = super(UserProfile, self).get_form(request, obj=None, **kwargs)
        
        if not request.user.is_superuser:
            form.base_fields['user'].queryset = form.base_fields['user'].queryset.filter(id=request.user.id)
        
        form.base_fields['user'].initial = request.user
        
        return form



admin.site.register(models.UserProfile,UserProfile)
