from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect 
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from Job.models import Job
from  django.core.mail import EmailMessage
from .forms import ApplicationEditForm, ApplicationForm
from .models import Application
from django.template.loader import render_to_string
from twilio.rest import Client 
from .tasks import send_email_notification,send_sms_notification
from datetime import datetime
# Create your views here.


class ApplicationCreateView(LoginRequiredMixin,SuccessMessageMixin, CreateView):
    model = Application
    template_name = "applications/add-application.html"
    form_class = ApplicationForm
    success_message = "Job Application Success!"

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['slug'] = self.kwargs['slug']  # pass job slug to form
    #     # kwargs['job'] = get_object_or_404(Job, slug=self.kwargs['slug'])
    #     return kwargs

    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        slug = self.kwargs["slug"]
        f.job = Job.objects.get(slug=slug)
        f.save()
        return super(ApplicationCreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("applications:my-applications")


class ApplicationDetailView(LoginRequiredMixin,DetailView):
    model = Application
    template_name = "applications/application-detail.html"
    context_object_name = "application"
    slug_field = "uuid"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class MyApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "applications/my-applications.html"
    context_object_name = "applications"
    paginate_by = 1000

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("user", "job")
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["paginator"] = Paginator(context["object_list"], self.paginate_by)
        return context


class ApplicationUpdateView(LoginRequiredMixin,UpdateView):
    model = Application
    template_name = "applications/update-applications.html"
    form_class = ApplicationEditForm

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset, uuid=self.kwargs.get("slug"), user=self.request.user
        )

        return obj

    def get_success_url(self):
        return reverse_lazy("applications:my-applications")


class ApplicationDeleteView(DeleteView):
    model = Application
    template_name = "applications/delete-application.html"

    def get_success_url(self):
        return reverse_lazy("applications:my-applications")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user, pk=self.kwargs["pk"])







class ApplicationRejectView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Application
    fields = ["status"]
    template_name_suffix = "_reject_form"
    def test_func(self):
        application = self.get_object()
        return self.request.user == application.user
    
    def form_valid(self, form):
        job = self.object.job
        new_status = form.cleaned_data["status"]
        
        if new_status == "Rejected": #and self.object.status == "Accepted":
            job.status = "Open"
            Application.objects.filter(job=job, status="Not Accepted").exclude(
                pk=self.object.pk
            ).update(status="Pending")
            # sending email notification
            job_owner_email =self.object.job.user.email
            # job_owner_email='victorobwaku@gmail.com'
            subject = 'Approved Application Rejected'
            context ={
                'job':job,
                'application': self.get_object(),
                'applicant':self.get_object().user
            }
            message = render_to_string('emails/reject-accepted-application.html',context)           
            send_email_notification.delay(subject,message,job_owner_email)
            print(job_owner_email,job.title)
           
            
            # sending sms notification
            # twilio_message = f"Congratulations! Your application for the job '{job.title}' has been accepted."  # Compose the message
            # job_owner_phone_number="9876667"
            # send_sms_notification.delay(twilio_message,job_owner_phone_number)
        else:
            self.object.status = new_status
            self.object.approved_canceled_time= datetime.now()

        self.object.save()
        job.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            "applications:my-applications")

   
class ApplicationApprovalAcceptedView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Application
    fields = ["status"]
    template_name_suffix = "_accept_form"
    
    def test_func(self):
        application = self.get_object()
        return self.request.user == application.user
    
    def form_valid(self, form):
        job = self.object.job
        new_status = form.cleaned_data["status"]
       
        if new_status == "AcceptJob": #and self.object.status == "Accepted":
            job.status = "In Progress"
            Application.objects.filter(job=job, status="Not Accepted").exclude(
                pk=self.object.pk
            ).update(status="Failed")
            
            # sending email notification
            job_owner_email =self.get_object().job.user.email
            # job_owner_email='victorobwaku@gmail.com'
            subject = 'Application Accepted'
            context ={
                'job':job,
                'application': self.object,
                'applicant':self.object.user
            }
            message = render_to_string('emails/accept-accepted-application.html',context)
            send_email_notification.delay(subject,message,job_owner_email)
            print(job_owner_email,job.title)
            
            # sending sms notification
            
            # twilio_message = f"Congratulations! Your application for the job '{job.title}' has been accepted."  # Compose the message
            # job_owner_phone_number="9876667"
            # send_sms_notification.delay(twilio_message,job_owner_phone_number)
        else:
            self.object.status = new_status
            self.object.approved_canceled_time= datetime.now()

        self.object.save()
        job.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            "applications:my-applications"
        )

# def Ratings(request):
#      return (render,'ratings/ratings.html')