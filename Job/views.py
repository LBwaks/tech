from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from .models import Category,Job,JobImage
from django.views.generic import ListView,DetailView,CreateView
from django.shortcuts import get_object_or_404
from .forms import JobForm
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.


class JobListView(ListView):
    model = Job
    template_name = "jobs/jobs.html"
    

class JobDetailView(DetailView):
    model = Job
    template_name = "jobs/job-details.html"
    
    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context['job']= get_object_or_404(Job,slug=self.kwargs.get("slug"))
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
    
 