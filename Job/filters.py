from datetime import datetime, timedelta

import django_filters
from django import forms
from django.shortcuts import render
from taggit.models import Tag

from .choices import COUNTY, INDUSTRY, JOB_TYPE, PUBLISHED, SEEKER_TYPE
from .models import Category, Job


class JobFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    tags = django_filters.ModelChoiceFilter(queryset=Tag.objects.all())
    county = django_filters.ChoiceFilter(choices=COUNTY)
    # location = django_filters.CharFilter(lookup_expr="iexact", field_name="location")
    job_type = django_filters.MultipleChoiceFilter(
        choices=JOB_TYPE,
        widget=forms.RadioSelect
    )
    industry = django_filters.ChoiceFilter(
        choices=INDUSTRY,
    )
    seeker_type = django_filters.MultipleChoiceFilter(
        choices=SEEKER_TYPE, widget=forms.RadioSelect
    )
    # created= django_filters.ChoiceFilter(choices=PUBLISHED,method="filter_date_created")

    def filter_date_created(self, queryset, name, value):
        now = datetime.now()

        if value == "hour":
            start_time = now - timedelta(hours=1)
            queryset = queryset.filter(created__gte=start_time)
        elif value == "day":
            start_time = now - timedelta(days=1)
            queryset = queryset.filter(created__gte=start_time)
        elif value == "week":
            start_time = now - timedelta(days=7)
            queryset = queryset.filter(created__gte=start_time)

        elif value == "month":
            start_time = now - timedelta(days=30)
            queryset = queryset.filter(created__gte=start_time)
        return queryset

    class Meta:
        model = Job
        fields = [
            "category",
            "tags",
            "industry",
            "county",
            # "location",
            "job_type",
            "seeker_type",
        ]


# def job_list(request):
#     job_filter = JobFilter(request.GET, queryset=Job.objects.all())
#     return render(request, 'jobs/job.html', {'filter': job_filter})
