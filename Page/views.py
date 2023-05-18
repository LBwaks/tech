from django.contrib.postgres.search import (SearchHeadline, SearchQuery,
                                            SearchRank, SearchVector)
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView, ListView, TemplateView
from taggit.models import Tag
from django.core.paginator import Paginator
from Job.models import Job

from .forms import JobSearchForm

# Create your views here.


class Home(TemplateView):
    template_name = "pages/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        return context
    
    

class JobSearchView(ListView):
    model = Job
    template_name = "pages/search.html"
    context_object_name ='results'    
    paginate_by =5
    form = JobSearchForm()

    
    def  get_queryset(self):
        queryset = super().get_queryset().select_related('category', 'user').prefetch_related('tags')
        tag =self.request.GET.get('tag')
        title= self.request.GET.get('title')
        location = self.request.GET.get('location')      
        
        if tag != '0':
            tag= get_object_or_404(Tag,pk=tag)
            queryset = queryset.filter(Q(tags__name__icontains=tag.name)|Q(tags=tag))
         
        # if title :
        #         search_vector =SearchVector('title',weight="A")
        
        #         search_query =SearchQuery(title)
        #         search_headline = SearchHeadline('title',search_query)
        #         queryset = queryset.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).annotate(headline=search_headline).filter(rank__gte=0.3).order_by('-rank')
           
        if title :
            search_vector =SearchVector('title',weight="A")
            search_query =SearchQuery(title)
            search_headline = SearchHeadline('title',search_query)
            queryset = queryset.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).annotate(headline=search_headline).order_by('-rank')
        if location:
            search_vector =(
                SearchVector('county',weight="A")
                +SearchVector('location',weight="B")
                +SearchVector('address',weight="B"))
            search_query=SearchQuery(location)
            search_headline=SearchHeadline('location',search_query)
            queryset = queryset.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).annotate(headline=search_headline).order_by('-rank')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["form"] = JobSearchForm()
        context['tag'] = self.request.GET.get('tag',None)
        context['title']= self.request.GET.get('title',None)
        context['location'] =self.request.GET.get('location',None)
        
        paginator = Paginator(context['results'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)        
        context['page_obj'] = page_obj
        
        return context
    
    

    
