from typing import Any
from django.contrib import admin
from .models import Category,Job,JobImage,Complaints

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ('name','description','is_published','created_date')
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ('user',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
    def save_model(self, request, obj, form, change) :
        if not obj.user_id:
            obj.user = request.user
            obj.save()
        return super().save_model(request, obj, form, change)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    '''Admin View for Job'''

    list_display = ('reference_id','id','title','deadline','created')
    list_filter = ('tags','skills')
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ('user','reference_id')
    search_fields = ('reference_id','title')
    # date_hierarchy = ''
    # ordering = ('',)
    def save_model(self, request, obj, form, change) :
        if not obj.user_id:
            obj.user = request.user
            obj.save()
        return super().save_model(request, obj, form, change)

@admin.register(JobImage)
class JobImageAdmin(admin.ModelAdmin):
    '''Admin View for JobImage'''

    list_display = ('job','created')
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
@admin.register(Complaints)
class ComplaintsyAdmin(admin.ModelAdmin):
    '''Admin View for Complaintsy'''

    list_display = ('title','subject','created')
    
    readonly_fields = ('user',)
    
    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.user = request.user
        return super().save_model(request, obj, form, change)