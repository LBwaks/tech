from django.shortcuts import render
import django_filters
from .models import Job ,Category
from taggit.models import Tag
from datetime import datetime,timedelta
from .choices import COUNTY, JOB_TYPE, SEEKER_TYPE,INDUSTRY,PUBLISHED

class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains' ,field_name='title')
    category =django_filters.ModelChoiceFilter(queryset = Category.objects.all())
    tags = django_filters.ModelMultipleChoiceFilter(queryset = Tag.objects.all())
    county = django_filters.ChoiceFilter(choices = COUNTY)
    location =django_filters.CharFilter(lookup_expr='iexact' ,field_name='location')   
    job_type =django_filters.ChoiceFilter(choices = JOB_TYPE)
    industry =django_filters.ChoiceFilter(choices = INDUSTRY)
    seeker_type =django_filters.ChoiceFilter(choices = SEEKER_TYPE)
    created= django_filters.ChoiceFilter(choices=PUBLISHED,method="filter_date_created")
    
    def filter_date_created(self,queryset,name,value):
        now=datetime.now()
        
        if value =='hour':
            start_time = now-timedelta(hours=1)
            queryset = queryset.filter(created__gte=start_time)
        elif value =='day':
            start_time = now-timedelta(days=1)
            queryset = queryset.filter(created__gte=start_time)
        elif value =='week':
            start_time = now-timedelta(days=7)
            queryset = queryset.filter(created__gte=start_time)
            
        elif value =='month':
            start_time =now-timedelta(days=30)
            queryset = queryset.filter(created__gte=start_time)
        return queryset
    class Meta:
        model = Job        
        fields =['title','category' ,'tags', 'industry','county' , 'location' ,'job_type' ,'seeker_type','created']
        
# def job_list(request):
#     job_filter = JobFilter(request.GET, queryset=Job.objects.all())
#     return render(request, 'jobs/job.html', {'filter': job_filter})
