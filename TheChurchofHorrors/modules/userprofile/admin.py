# coding=utf-8

import models

from django.contrib import admin

class UserProfileItem(admin.TabularInline):
    model = models.UserProfileItem
    can_delete = True
    extra = 1

class UserProfile(admin.ModelAdmin):
    model = models.UserProfile
    
    inlines = (UserProfileItem,)



admin.site.register(models.UserProfile,UserProfile)
