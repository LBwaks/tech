from typing import Any, Optional
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from .models import Application
from django.views.generic import CreateView,DetailView,UpdateView,ListView,DeleteView
from django.core.paginator import Paginator
from .forms import ApplicationForm,ApplicationEditForm
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from Job.models import Job
from django.urls import reverse_lazy,reverse
# Create your views here.

class ApplicationCreateView(SuccessMessageMixin,CreateView):
    model = Application
    template_name = "applications/add-application.html"
    form_class = ApplicationForm
    success_message ='Job Application Success!'
    
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['slug'] = self.kwargs['slug']  # pass job slug to form
    #     # kwargs['job'] = get_object_or_404(Job, slug=self.kwargs['slug'])
    #     return kwargs
    
    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        slug = self.kwargs['slug']
        f.job = Job.objects.get(slug=slug)  
        f.save()
        return super(ApplicationCreateView,self).form_valid(form)



class ApplicationDetailView(DetailView):
    model = Application
    template_name = "applications/application-details.html"
    context_object_name = 'application'
    slug_field = 'uuid'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    

class MyApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'applications/my-applications.html'
    context_object_name = 'applications'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user', 'job')
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['paginator'] = Paginator(context['object_list'], self.paginate_by)
        return context


class ApplicationUpdateView(UpdateView):
    model = Application
    template_name = 'applications/update-applications.html'
    form_class = ApplicationEditForm
    
    def get_object(self, queryset = None ):
        if queryset is None:
            queryset= self.get_queryset()
        obj = get_object_or_404(queryset,uuid=self.kwargs.get('slug'), user=self.request.user)
            
        return obj
    
    def get_success_url(self):
        return reverse_lazy('application-details', kwargs={'slug': self.object.uuid})
    
class ApplicationDeleteView(DeleteView):
    model = Application
    template_name = 'applications/delete-application.html'
    
    
    def get_success_url(self):
        return reverse('jobs')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user, pk=self.kwargs['pk'])
