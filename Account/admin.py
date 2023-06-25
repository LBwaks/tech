from typing import Any
from django.contrib import admin
from .models import Profile,ProfileCV,Rating
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Admin View for Profile'''

    list_display = ('user','firstname','lastname','id_passport','status','is_suspended','created',)
    list_filter = ('title','skills','county',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ('slug',)
    # search_fields = ('',)
    # date_hierarchy = ''
    ordering = ('-created',)
    
    # def save_model(self, request, obj, form, change):
    #     if not obj.user_id:
    #         obj.user = request.user
    #         obj.save()
    #     return super().save_model(request, obj, form, change)

@admin.register(ProfileCV)
class ProfileCVAdmin(admin.ModelAdmin):
    '''Admin View for ProfileCV'''

    list_display = ('profile','cv','created')
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    '''Admin View for Rating'''

    list_display = ('ratings','profile_id','reviews')
   