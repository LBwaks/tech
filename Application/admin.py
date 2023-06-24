from typing import Any
from django.contrib import admin
from .models import Application,Rating
# Register your models here.
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    '''Admin View for Application'''

    list_display = ('uuid','user','charge','description')
    # list_filter = ('',)
    # inlines = [
    #     Inline,
    # ]
    # raw_id_fields = ('',)
    readonly_fields = ('uuid','user')
    # search_fields = ('',)
    # date_hierarchy = ''
    # ordering = ('',)
    def save_model(self, request,obj, form, change):
        if not obj.user_id:
            obj.user = request.user
            obj.save()
            
        return super().save_model(request,obj, form, change)
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    '''Admin View for Rating'''

    list_display = ('ratings','application_id','reviews')
   