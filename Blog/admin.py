from typing import Any
from django.contrib import admin
from .models import Category,Blog,Comment
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ('name',"is_published","is_featured","created_date")
    readonly_fields = ('user',)
    def save_model(self, request, obj, form, change):
        obj.user=request.user
        return super().save_model(request, obj, form, change)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    '''Admin View for Blog'''

    list_display = ('title',"category",'is_published','created')
    list_filter = ("category",)
    
    readonly_fields = ('user',)
    search_fields = ('name',)
    # date_hierarchy = ''
    ordering = ('-created',)
    
    def save_model(self, request, obj, form, change):
        obj.user=request.user
        return super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''Admin View for Comment'''

    list_display = ('blog','user','comment','parent','created')
    
    # ordering = ('',)