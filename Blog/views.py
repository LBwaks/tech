from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Blog
# Create your views here.
class BlogListView(ListView):
    model = Blog
    template_name = "blogs/blogs.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("category","user").prefetch_related("tags")        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context[""] = 
        return context
    
