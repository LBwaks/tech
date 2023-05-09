from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
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

from Job.models import Job

from .forms import ApplicationEditForm, ApplicationForm
from .models import Application

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
    paginate_by = 10

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
            job.status = "In progress"
            Application.objects.filter(job=job).exclude(pk=self.object.pk).update(
                status="Not Accepted"
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
