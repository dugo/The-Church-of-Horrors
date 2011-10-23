# coding=utf-8

import models

from django.contrib import admin

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



admin.site.register(models.UserProfile,UserProfile)
