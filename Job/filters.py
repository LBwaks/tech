from django.shortcuts import render
import django_filters
from .models import Job ,Category
from taggit.models import Tag
from .choices import COUNTY, JOB_TYPE, SEEKER_TYPE

class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains' ,field_name='title')
    category =django_filters.ModelChoiceFilter(queryset = Category.objects.all())
    tags = django_filters.ModelMultipleChoiceFilter(queryset = Tag.objects.all())
    county = django_filters.ChoiceFilter(choices = COUNTY)
    location =django_filters.CharFilter(lookup_expr='iexact' ,field_name='location')   
    job_type =django_filters.ChoiceFilter(choices = JOB_TYPE)
    seeker_type =django_filters.ChoiceFilter(choices = SEEKER_TYPE)
    
    class Meta:
        model = Job        
        fields =['title','category' ,'tags' ,'county' , 'location' ,'job_type' ,'seeker_type']
        
def job_list(request):
    job_filter = JobFilter(request.GET, queryset=Job.objects.all())
    return render(request, 'jobs/job.html', {'filter': job_filter})
