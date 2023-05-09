from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from .models import Category,Job,JobImage,SavedJob
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.shortcuts import get_object_or_404
from .forms import JobForm,JobEditForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.text import slugify
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from taggit.models import Tag
from django.db.models import Prefetch
from django_filters.views import FilterView
from .filters import JobFilter
from Application.models import Application
# Create your views here.


class JobListView(ListView):
    model = Job
    template_name = "jobs/jobs.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = JobFilter(self.request.GET, queryset=self.get_queryset())
        return context
    

class JobDetailView(DetailView):
    model = Job
    template_name = "jobs/job-details.html"
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['job'] = self.object
       return context

class JobCreateView(SuccessMessageMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/add-jobs.html"
    success_message ='Job Posted Successfully !'
    
    def form_valid(self, form) :
        job = form.save(commit=False)
        job.user = self.request.user
        job.save()
        images = self.request.FILES.getlist('images')
        for image in images:
            JobImage.objects.create(job=job,image=image)
        return super(JobCreateView,self).form_valid(form)

class JobUpdateView(SuccessMessageMixin,UpdateView):
    model = Job
    template_name = "jobs/update-jobs.html"
    form_class = JobEditForm
    success_message ='Job Edited Successfully !'
    
    def form_valid(self, form) :
        job = form.save(commit=False)
        images = self.request.FILES.getlist('images')
        for image in images:
            JobImage.objects.create(job=job, image=image)
        self.object = form.save()
        form.save_m2m() # Save many-to-many relationships
        return super(JobUpdateView,self).form_valid(form)


class JobDeleteView(SuccessMessageMixin,DeleteView):
    model = Job
    template_name = "jobs/delete-jobs.html"
    success_message ='Job deete Successfully !'
    success_url = reverse_lazy("jobs") # add your custom URL here

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    

@login_required
# @require_POST
def savedJob(request,slug):
    job= get_object_or_404(Job,slug=slug)
    saved_job ,created= SavedJob.objects.get_or_create(user=request.user,job=job)
    if not created:
        saved_job.delete()
        message ='Unsaved ' 
    else:
        message ='saved'
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
    

class SavedJobListView(ListView):
    model = SavedJob
    template_name = "jobs/saved-jobs.html"
    context_object_name = 'jobs'
    paginate_by = 10 
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            cache_key = f'saved_jobs_{user.id}'
            saved_jobs = cache.get(cache_key)
            if not saved_jobs:
                saved_jobs = SavedJob.objects.select_related('job', 'job__category').prefetch_related('job__tags').filter(user=user).order_by('-saved_date')
                cache.set(cache_key, saved_jobs)
            return saved_jobs
        return []
        
class MyJobListView(ListView):
    template_name = 'jobs/my-jobs.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            cache_key = f'my_jobs_{user.id}_{self.request.GET.get("q", "")}'
            jobs = cache.get(cache_key)
            if not jobs:
                query = Q(user=user)
                search_term = self.request.GET.get('q', '').strip()
                if search_term:
                    query &= Q(title__icontains=search_term) | Q(content__icontains=search_term) | Q(tags__name__icontains=search_term)
                jobs = Job.objects.filter(query).select_related('category').prefetch_related('tags').order_by('-created')
                cache.set(cache_key, jobs)
            return jobs.values('id', 'title', 'slug', 'category__name', 'created')
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('q', '').strip()
        return context
    
class JobsByUserView(ListView):
    template_name = 'jobs/user-jobs.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        self.username = self.kwargs.get('username')
        slugified_username = slugify(self.username)  # Convert username to a valid slug
        user = User.objects.filter(username=slugified_username).first()
        if not user:
            return Job.objects.none()
        return Job.objects.filter(user=user).select_related('category').prefetch_related('tags').order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.username
        return context
class JobsByCategoryView(ListView):
    model = Job
    template_name = 'jobs/category-jobs.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Job.objects.filter(category=self.category).select_related('category').prefetch_related('tags').order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    
class JobsByTagView(ListView):
    model = Job
    template_name = 'jobs/tag-jobs.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        tag_slug = self.kwargs.get('slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        return Job.objects.filter(tags=tag).select_related('category').prefetch_related('tags').order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return context

class JobFilterView(FilterView):
    model = Job
    template_name ='jobs/jobs.html'
    filterset_class= JobFilter
    paginate_by =10
    
    def get_queryset(self):
        return super().get_queryset().select_related('category').prefetch_related('tags').order_by('-created')

class JobApplicationsListView(ListView):
    model = Application
    context_object_name = 'applications'
    template_name = 'applications/job-applications.html'
    paginate_by = 10
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        job = get_object_or_404(Job, slug=slug)
        return job.job_application.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['job'] = get_object_or_404(Job, slug=slug)
        return context
