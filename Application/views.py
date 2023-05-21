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
    template_name = "applications/application-details.html"
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
        return reverse_lazy("application-details", kwargs={"slug": self.object.uuid})


class ApplicationDeleteView(DeleteView):
    model = Application
    template_name = "applications/delete-application.html"

    def get_success_url(self):
        return reverse("jobs")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user, pk=self.kwargs["pk"])


class ApplicationStatusUpdateView(UpdateView):
    model = Application
    fields = ["status"]
    template_name_suffix = "_status_form"

    def form_valid(self, form):
        job = self.object.job
        new_status = form.cleaned_data["status"]
        if new_status == "Accepted":
            job.status = "Waiting"
            Application.objects.filter(job=job).exclude(pk=self.object.pk).update(
                status="Not Accepted"
            )
            # sending email notification
            applicant_email =self.object.user.email
            applicant_email ='victorobwaku@gmail.com'
            subject = 'Application Accepted'
            context ={
                'job':job,
                'application': self.object,
                'applicant':self.object.user
            }
            message = render_to_string('emails/application-approved.html',context)
            # email = EmailMessage(subject,message,settings.DEFAULT_FROM_EMAIL,[applicant_email])
            # email.content_subtype = "html"
            # email.send()
            # print(applicant_email,job.title)
            send_email_notification.delay(subject,message,applicant_email)
            
            # sending sms notification
            # twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)  # Initialize Twilio client
            # twilio_phone = settings.TWILIO_PHONE_NUMBER  # Get Twilio phone number from settings
             # twilio_client.messages.create(
            #     body=twilio_message,
            #     from_='+15005550006',
            #     to='+254797407274'
            # )
            
            # use this
            # twilio_message = f"Congratulations! Your application for the job '{job.title}' has been accepted."  # Compose the message
                      
            # recipient_phone_number ='+245342323'
            # send_sms_notification.delay(twilio_message,recipient_phone_number)
            
        else:
            self.object.status = new_status
        self.object.save()
        job.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            "applications:job_applications", kwargs={"slug": self.object.job.slug}
        )

class ApplicationCancelView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    fields = ["status"]
    template_name_suffix = '_confirm_delete'
    
    def test_func(self):
        application = self.get_object()
        return self.request.user == application.job.user
    
    def form_valid(self, form):
        job = self.object.job
        new_status = form.cleaned_data["status"]
        if new_status == "Pending":
            job.status = "Open"
            Application.objects.filter(job=job).exclude(pk=self.object.pk).update(
                status="Pending"
            )
            # sending email notification
            applicant_email =self.object.user.email
            subject = 'Application Accepted'
            context ={
                'job':job,
                'application': self.object,
                'applicant':self.object.user
            }
            message = render_to_string('emails/cancel-accepted-application.html',context)
            email = EmailMessage(subject,message,settings.DEFAULT_FROM_EMAIL,[applicant_email])
            email.content_subtype = "html"
            email.send()
            print(applicant_email,job.title)
            
            # sending sms notification
            twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)  # Initialize Twilio client
            # twilio_phone = settings.TWILIO_PHONE_NUMBER  # Get Twilio phone number from settings
            twilio_message = f"Congratulations! Your application for the job '{job.title}' has been accepted."  # Compose the message
            twilio_client.messages.create(
                body=twilio_message,
                from_='+15005550006',
                to='+254797407274'
            )
        else:
            self.object.status = new_status
        self.object.save()
        job.save()
        return super().form_valid(form)
    
    
    
    def get_success_url(self):
        return reverse_lazy('applications:job_applications', kwargs={'slug': self.object.job.slug})
   


class ApplicationRejectView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Application
    fields = ["status"]
    template_name_suffix = "_reject_form"
    def test_func(self):
        application = self.get_object()
        return self.request.user == application.job.user
    
    def form_valid(self, form):
        job = self.object.job
        new_status = form.cleaned_data["status"]
        
        if new_status == "Rejected": #and self.object.status == "Accepted":
            job.status = "Open"
            Application.objects.filter(job=job, status="Not Accepted").exclude(
                pk=self.object.pk
            ).update(status="Pending")
            # sending email notification
            applicant_email =self.object.user.email
            subject = 'Application Accepted'
            context ={
                'job':job,
                'application': self.object,
                'applicant':self.object.user
            }
            message = render_to_string('emails/reject-accepted-application.html',context)
            email = EmailMessage(subject,message,settings.DEFAULT_FROM_EMAIL,[applicant_email])
            email.content_subtype = "html"
            email.send()
            print(applicant_email,job.title)
            
            # sending sms notification
            twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)  # Initialize Twilio client
            # twilio_phone = settings.TWILIO_PHONE_NUMBER  # Get Twilio phone number from settings
            twilio_message = f"Congratulations! Your application for the job '{job.title}' has been accepted."  # Compose the message
            twilio_client.messages.create(
                body=twilio_message,
                from_='+15005550006',
                to='+254797407274'
            )
        else:
            self.object.status = new_status

        self.object.save()
        job.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            "applications:job_applications", kwargs={"slug": self.object.job.slug}
        )

   
class ApplicationApprovalAcceptedView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Application
    fields = ["status"]
    template_name_suffix = "_reject_form"
    def test_func(self):
        application = self.get_object()
        return self.request.user == application.job.user
    
    def form_valid(self, form):
        job = self.object.job
        new_status = form.cleaned_data["status"]
        # if new_status == "Accepted":
        #     job.status = "In progress"
        #     Application.objects.filter(job=job).exclude(pk=self.object.pk).update(
        #         status="Not Accepted"
        #     )
        if new_status == "AcceptJob": #and self.object.status == "Accepted":
            job.status = "In Progress"
            Application.objects.filter(job=job, status="Not Accepted").exclude(
                pk=self.object.pk
            ).update(status="Failed")
            # sending email notification
            applicant_email =self.object.user.email
            subject = 'Application Accepted'
            context ={
                'job':job,
                'application': self.object,
                'applicant':self.object.user
            }
            message = render_to_string('emails/accept-accepted-application.html',context)
            email = EmailMessage(subject,message,settings.DEFAULT_FROM_EMAIL,[applicant_email])
            email.content_subtype = "html"
            email.send()
            print(applicant_email,job.title)
            
            # sending sms notification
            twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)  # Initialize Twilio client
            # twilio_phone = settings.TWILIO_PHONE_NUMBER  # Get Twilio phone number from settings
            twilio_message = f"Congratulations! Your application for the job '{job.title}' has been accepted."  # Compose the message
            twilio_client.messages.create(
                body=twilio_message,
                from_='+15005550006',
                to='+254797407274'
            )
        else:
            self.object.status = new_status

        self.object.save()
        job.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            "applications:job_applications", kwargs={"slug": self.object.job.slug}
        )
