from datetime import datetime
from random import random
from django.contrib.postgres.search import (SearchHeadline, SearchQuery,
                                            SearchRank, SearchVector)
from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView, ListView, TemplateView,FormView,DetailView
from taggit.models import Tag
from django.core.paginator import Paginator
from Job.models import Job
from.models import Contact,Faq,Service
from django.urls import reverse
from .forms import JobSearchForm,ContactForm
from django.template.loader import render_to_string
from django.core.mail import BadHeaderError,EmailMultiAlternatives
from Page.tasks import send_contact_email
from django.db.models import Count
from Blog.models import Blog
# Create your views here.


class Home(TemplateView):
    template_name = "pages/home.html"
    model = Job
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # tags
        tags = Tag.objects.all()
         # featured_jobs
        #  .filter(status="Open",deadline__gte=datetime.now())
        featured_jobs = Job.objects.select_related('user','category').prefetch_related('tags').filter(is_featured=True,status="Open",deadline__gte=datetime.now())[:6]
        
         # recent_jobs 
        recent_jobs = Job.objects.select_related('user','category').prefetch_related('tags').filter(status="Open",deadline__gte=datetime.now()).order_by('-created')[:6]
        
        # popular_jobs.
        popular_jobs = Job.objects.select_related('user','category').prefetch_related('tags').filter(status="Open",deadline__gte=datetime.now()).order_by('-hit_count_generic__hits')[:6]
        
        popular_tags  =Tag.objects.annotate(num_jobs=Count('job')).order_by('-num_jobs')[:5]
        blogs = Blog.objects.select_related('user','category').order_by('-created')[:3]
        
        context={'blogs':blogs, 'tags':tags,'featured_jobs':featured_jobs,'recent_jobs':recent_jobs,'popular_jobs':popular_jobs,'popular_tags':popular_tags}
        
        return context
    

    

class JobSearchView(ListView):
    model = Job
    template_name = "pages/search.html"
    context_object_name ='results'    
    paginate_by =5
    form = JobSearchForm()

    
    def  get_queryset(self):
        queryset = super().get_queryset().select_related('category', 'user').prefetch_related('tags').filter(status="Open",deadline__gte=datetime.now())
        tag =self.request.GET.get('tag')
        title= self.request.GET.get('title')
        location = self.request.GET.get('location')      
        
        if tag and tag != '0':
            tag= get_object_or_404(Tag,pk=tag)
            queryset = queryset.filter(Q(tags__name__icontains=tag.name)|Q(tags=tag))
         
       
        if title :
            search_vector =SearchVector('title',weight="A")
            search_query =SearchQuery(title)
            search_headline = SearchHeadline('title',search_query)
            queryset = queryset.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).annotate(headline=search_headline).order_by('-rank')
            
        if location:
            search_vector =(
                SearchVector('county',weight="A")
                +SearchVector('location',weight="B")
                +SearchVector('address',weight="B"))
            search_query=SearchQuery(location)
            search_headline=SearchHeadline('location',search_query)
            queryset = queryset.annotate(search=search_vector,rank=SearchRank(search_vector,search_query)).annotate(headline=search_headline).order_by('-rank')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["form"] = JobSearchForm()
        tag_id =self.request.GET.get('tag',None)
        if tag_id == '0':
            context['tag'] = 'All Tags'
        elif tag_id is not None:
            tag = get_object_or_404(Tag, pk=tag_id)
            context['tag'] = tag.name  # Assuming the tag has a 'name' field
        else:
            context['tag'] = 'All'  # Default value if no tag is selected

        context['title']= self.request.GET.get('title',None)
        context['location'] =self.request.GET.get('location',None)
        context['total_results']= context['paginator'].count
        
        paginator = Paginator(context['results'], self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)        
        context['page_obj'] = page_obj
        
        return context
    
    

    
# class HomeView(ListView):
#     template_name = 'home.html'
#     context_object_name = 'jobs'
#     paginate_by = 10

#     def get_queryset(self):
#         # Get featured jobs (assuming featured jobs have is_featured=True)
#         featured_jobs = Job.objects.filter(is_featured=True)

#         # Get recent jobs (assuming recent jobs are sorted by creation date)
#         recent_jobs = Job.objects.filter(is_published=True).order_by('-created')

#         # Get popular jobs (assuming popular jobs are sorted by positions)
#         popular_jobs = Job.objects.filter(is_published=True).order_by('-positions')

#         # Get random 5 jobs from each category
#         random_featured_jobs = random.sample(list(featured_jobs), min(5, len(featured_jobs)))
#         random_recent_jobs = random.sample(list(recent_jobs), min(5, len(recent_jobs)))
#         random_popular_jobs = random.sample(list(popular_jobs), min(5, len(popular_jobs)))

#         # Combine the job lists
#         job_list = random_featured_jobs + random_recent_jobs + random_popular_jobs

#         return job_list


class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    model= Contact
    # success_url = "contact"
    def get_success_url(self):
        return reverse('contact')
    
    def form_valid(self,form):
        name = form.cleaned_data.get("name")
        from_email = form.cleaned_data.get('email')
        subject = form.cleaned_data.get('subject')
        # message = f'{name} with email {from_email} said :\n'
        # message += f'Subject :"{subject}" \n\n'
        message = form.cleaned_data.get('message')
        
        # context = {
        #     'name':name,
        #     'email':from_email,
        #     'subject':subject,
        #     'message':message
        # } 
        # print(context)
        # text_content = render_to_string('emails/contact-email.html',context)
        # html_content= render_to_string('emails/contact-email.html',context)
        # try : 
        #     mail= EmailMultiAlternatives(
        #         subject=subject,
        #         body=message,
        #         from_email=from_email,
        #         to=['victorobwaku@gmail.com']
        #     ) 
        #     mail.attach_alternative(html_content,'text/html')
        #     mail.send(fail_silently=False)
        #     print('sent')
        # except BadHeaderError:
        #     return self.form_invalid(form)
        send_contact_email.delay(name,from_email,subject,message)
        return super().form_valid(form)


def error_404(request,exception):
    return render (request, 'errors/404.html',status=404)

def error_500(request):
    return render (request, 'errors/500.html')


class FaqListView(ListView):
    model = Faq
    template_name = "pages/faqs.html"
    context_object_name = 'faqs'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["faqs"] = self.get_queryset
        return context

class About(ListView):
    model = Service
    template_name = "pages/about.html"
    context_object_name='services'
    
    def get_queryset(self):
        queryset=super().get_queryset()
        queryset = queryset.select_related('user')
        return super().get_queryset()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = self.get_queryset()
        return context
    
    
