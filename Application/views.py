from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.conf import settings
from Job.models import Job
from  django.core.mail import EmailMessage
from .forms import ApplicationEditForm, ApplicationForm
from .models import Application
from django.template.loader import render_to_string

# Create your views here.


class ApplicationCreateView(SuccessMessageMixin, CreateView):
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


class ApplicationDetailView(DetailView):
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


class ApplicationUpdateView(UpdateView):
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
            applicant_email =self.object.user.email
            subject = 'Application Accepted'
            context ={
                'job':job,
                'application': self.object,
                'applicant':self.object.user
            }
            message = render_to_string('emails/application-approved.html',context)
            email = EmailMessage(subject,message,settings.DEFAULT_FROM_EMAIL,[applicant_email])
            email.content_subtype = "html"
            email.send()
            print(applicant_email,job.title)
            
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
        else:
            self.object.status = new_status
        self.object.save()
        job.save()
        return super().form_valid(form)
    
    # def delete(self,request,*args, **kwargs):
    #     application = self.get_object()
    #     application.status = 'Not Accepted'
    #     application.job.status = 'Open'
    #     application.job.save()
    #     application.save()
    #     return self.redirect_to_success_url()
    
    def get_success_url(self):
        return reverse_lazy('applications:job_applications', kwargs={'slug': self.object.job.slug})
    from django.shortcuts import get_object_or_404


class ApplicationRejectView(UpdateView):
    model = Application
    fields = ["status"]
    template_name_suffix = "_reject_form"

    def form_valid(self, form):
        job = self.object.job
        new_status = form.cleaned_data["status"]
        # if new_status == "Accepted":
        #     job.status = "In progress"
        #     Application.objects.filter(job=job).exclude(pk=self.object.pk).update(
        #         status="Not Accepted"
        #     )
        if new_status == "Rejected": #and self.object.status == "Accepted":
            job.status = "Open"
            Application.objects.filter(job=job, status="Not Accepted").exclude(
                pk=self.object.pk
            ).update(status="Pending")
        else:
            self.object.status = new_status

        self.object.save()
        job.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            "applications:job_applications", kwargs={"slug": self.object.job.slug}
        )

   
class ApplicationApprovalAcceptedView(UpdateView):
    model = Application
    fields = ["status"]
    template_name_suffix = "_reject_form"

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
        else:
            self.object.status = new_status

        self.object.save()
        job.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            "applications:job_applications", kwargs={"slug": self.object.job.slug}
        )
