from typing import Any
from django.contrib import admin
from .models import Faq,Service
# Register your models here.
@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    '''Admin View for Faq'''

    list_display = ('title','category')
    readonly_fields=('user',)
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user= request.user
            obj.save()
            
        return super().save_model(request, obj, form, change)
    
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    '''Admin View for Service'''

    list_display = ('title',)
    readonly_fields=('user',)
    def save_model(self, request, obj, form, change) :
        if not obj.user_id:
            obj.user=request.user
            obj.save()
        return super().save_model(request, obj, form, change)