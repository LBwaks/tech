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
    model = Job
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # tags
        tags = Tag.objects.all()
         # featured_jobs
        featured_jobs = Job.objects.select_related('user','category').prefetch_related('tags').filter(is_featured=True)[:6]
        
         # recent_jobs 
        recent_jobs = Job.objects.select_related('user','category').prefetch_related('tags').order_by('-created')[:6]
        
        # popular_jobs.
        popular_jobs = Job.objects.select_related('user','category').prefetch_related('tags').order_by('-hit_count_generic__hits')[:6]
        
        
        context={'tags':tags,'featured_jobs':featured_jobs,'recent_jobs':recent_jobs,'popular_jobs':popular_jobs}
        
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
        tag_id =self.request.GET.get('tag',None)
        if tag_id == '0':
            context['tag'] = 'All Tags'
        elif tag_id is not None:
            tag = get_object_or_404(Tag, pk=tag_id)
            context['tag'] = tag.name  # Assuming the tag has a 'name' field
        else:
            context['tag'] = 'All'  # Default value if no tag is selected

        context['title']= self.request.GET.get('title',None)
        context['location'] =self.request.GET.get('location',None)
        context['total_results']= context['paginator'].count
        
        paginator = Paginator(context['results'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)        
        context['page_obj'] = page_obj
        
        return context
    
    

    
class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        # Get featured jobs (assuming featured jobs have is_featured=True)
        featured_jobs = Job.objects.filter(is_featured=True)

        # Get recent jobs (assuming recent jobs are sorted by creation date)
        recent_jobs = Job.objects.filter(is_published=True).order_by('-created')

        # Get popular jobs (assuming popular jobs are sorted by positions)
        popular_jobs = Job.objects.filter(is_published=True).order_by('-positions')

        # Get random 5 jobs from each category
        random_featured_jobs = random.sample(list(featured_jobs), min(5, len(featured_jobs)))
        random_recent_jobs = random.sample(list(recent_jobs), min(5, len(recent_jobs)))
        random_popular_jobs = random.sample(list(popular_jobs), min(5, len(popular_jobs)))

        # Combine the job lists
        job_list = random_featured_jobs + random_recent_jobs + random_popular_jobs

        return job_list
