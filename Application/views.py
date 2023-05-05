from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from .models import Application
from django.views.generic import CreateView,DetailView
from .forms import ApplicationForm
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from Job.models import Job
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
    
    def get_context_data(self, **kwargs):
        context = super(ApplicationDetailView, self).get_context_data(**kwargs)
        context['application']=get_object_or_404(Application,uuid=self.kwargs.get('slug'))
        return context
    
