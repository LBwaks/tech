import base64
import json
from typing import Any, Dict, Optional
from django import http
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
import requests
from .models import Category,Job,JobImage,SavedJob,Complaints
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,TemplateView
from django.shortcuts import get_object_or_404
from .forms import JobForm,JobEditForm ,RatingForm,ComplaintsForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.text import slugify
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from taggit.models import Tag
from django.db.models import Prefetch
from django_filters.views import FilterView
from .filters import JobFilter
from Application.models import Application
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from Job.tasks import update_job_expiry_status
from django.template.loader import render_to_string
from twilio.rest import Client 
from Job.tasks import send_email_notification,send_sms_notification
from django_daraja.mpesa.core import MpesaClient
from datetime import datetime
from django.db.models import Count
from hitcount.views import HitCountDetailView
from Account.models import Rating,Profile
from .generateAccessToken import get_access_token
# Create your views here.


class JobListView(ListView):
    model = Job
    template_name = "jobs/jobs.html"
    paginate_by = 10
    
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(status="Open",deadline__gte=datetime.now())
        queryset = queryset.select_related('category','user').prefetch_related('tags')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all()
        context['tags']=tags
        
        context['categories']=Category.objects.select_related('user')
        context['popular_tags'] =Tag.objects.annotate(num_jobs=Count('job')).order_by('-num_jobs')[:5]
        context['filter'] = JobFilter(self.request.GET, queryset=self.get_queryset())
        # update_job_expiry_status.delay()
        if self.request.user.is_authenticated:
            context['has_applied'] = set(Application.objects.filter(user=self.request.user).values_list("job__id",flat=True))
        return context
    
    # def dispatch(self, request, *args, **kwargs):
    #     update_job_expiry_status.delay()
    #     return super().dispatch(request, *args, **kwargs)
    
    

class JobDetailView(HitCountDetailView):
    model = Job
    template_name = "jobs/job-details.html"
    
    # @method_decorator(cache_page(60*15))    
    # def dispatch(self, request, *args, **kwargs):
    #     return super(JobDetailView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       job = self.get_object()
    #    has_user_applied = job.has_user_applied(self.request.user)
       if self.request.user.is_authenticated:
         context['has_applied']= Application.objects.filter(user=self.request.user,job=job).exists()
        # Get IDs of the tags associated with the current job
    #    tag_ids = job.tags.values_list('id', flat=True)
    #     # Fetch similar jobs based on category and tags
    #    similar_jobs =cache.get(f'similar_jobs_{job.id}')
        
       
    #    if similar_jobs is None:
    # #    fetch similar_jobs
    #      similar_jobs = Job.objects.select_related('category','user').prefetch_related('tags').filter(Q(category=job.category)|Q(tags__in=tag_ids)).exclude(id=job.id)[:5]
    #      cache.set(f'similar_job_{job.id}',similar_jobs,60*15)
       
       context['job']=job
    #    context['has_user_applied']=has_user_applied
    #    context['has_applied']=has_applied
    #    context['similar_jobs']=similar_jobs
       
       return context

class JobCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/add-jobs.html"
    success_message ='Job Posted Successfully !'
    
    def form_valid(self, form) :
        job = form.save(commit=False)
        job.user = self.request.user
        job.save()
        images = self.request.FILES.getlist('images')
        for image in images:
            JobImage.objects.create(job=job,image=image)
        return super(JobCreateView,self).form_valid(form)

class JobUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Job
    template_name = "jobs/update-jobs.html"
    form_class = JobEditForm
    success_message ='Job Edited Successfully !'
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(request,"You dont have permission to edit this job")
            return redirect(reverse('job-details',args=[obj.slug]))
            # raise  PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form) :
        job = form.save(commit=False)
        images = self.request.FILES.getlist('images')
        for image in images:
            JobImage.objects.create(job=job, image=image)
        self.object = form.save()
        form.save_m2m() # Save many-to-many relationships
        return super(JobUpdateView,self).form_valid(form)


class JobDeleteView(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model = Job
    template_name = "jobs/delete-jobs.html"
    success_message ='Job deete Successfully !'
    success_url = reverse_lazy("jobs") # add your custom URL here

    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(request,"You dont have permission to Delete  this job")
            return redirect(reverse('job-details',args=[obj.slug]))
            # raise  PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

    

@login_required
# @require_POST
def savedJob(request,slug):
    job= get_object_or_404(Job,slug=slug)
    saved_job= SavedJob.objects.filter(job=job, user=request.user).exists()
    # saved_job,created= SavedJob.objects.get_or_create(user=request.user,job=job)
    if saved_job:
        SavedJob.objects.filter(job=job,user=request.user).delete()        
        message ='Job UnBookmarked ' 
    else:
        message ='Bookmarked'
        SavedJob.objects.create(job=job,user=request.user)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
    

class SavedJobListView(LoginRequiredMixin,ListView):
    model = SavedJob
    template_name = "jobs/saved-jobs.html"
    context_object_name = 'jobs'
    paginate_by = 10 
    
    def get_queryset(self):
                user = self.request.user
        # if user.is_authenticated:
        #     cache_key = f'saved_jobs_{user.id}'
        #     saved_jobs = cache.get(cache_key)
        #     if not saved_jobs:
                saved_jobs = SavedJob.objects.select_related('job', 'job__category').prefetch_related('job__tags').filter(user=user).order_by('-saved_date')
                # cache.set(cache_key, saved_jobs)
                return saved_jobs
        # return []
        
class MyJobListView(LoginRequiredMixin,ListView):
    template_name = 'jobs/my-jobs.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            cache_key = f'my_jobs_{user.id}_{self.request.GET.get("q", "")}'
            jobs = cache.get(cache_key)
            if not jobs:
                query = Q(user=user)
                search_term = self.request.GET.get('q', '').strip()
                if search_term:
                    query &= Q(title__icontains=search_term) | Q(content__icontains=search_term) | Q(tags__name__icontains=search_term)
                jobs = Job.objects.filter(query).select_related('category').prefetch_related('tags').order_by('-created')
                cache.set(cache_key, jobs)
            return jobs
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('q', '').strip()
        return context
    
class JobsByUserView(ListView):
    template_name = 'jobs/user-jobs.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        self.username = self.kwargs.get('username')
        slugified_username = slugify(self.username)  # Convert username to a valid slug
        user = User.objects.filter(username=slugified_username).first()
        if not user:
            return Job.objects.none()
        return Job.objects.filter(user=user,status="Open",deadline__gte=datetime.now()).select_related('category').prefetch_related('tags').order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.username
        return context
class JobsByCategoryView(ListView):
    model = Job
    template_name = 'jobs/category-jobs.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Job.objects.filter(category=self.category,status="Open",deadline__gte=datetime.now()).select_related('category').prefetch_related('tags').order_by('-created')
# .filter(status="Open",deadline__gte=datetime.now())
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['caterory_name'] = self.category.name
        return context
    
class JobsByTagView(ListView):
    model = Job
    template_name = 'jobs/tag-jobs.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        tag_slug = self.kwargs.get('slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        return Job.objects.filter(tags=tag,status="Open",deadline__gte=datetime.now()).select_related('category').prefetch_related('tags').order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag=get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        context['tag'] = tag
        context['tag_name'] =tag.name
        return context

class JobFilterView(FilterView):
    model = Job
    template_name ='jobs/job-filter.html'
    filterset_class= JobFilter
    paginate_by =10
    
    def get(self, request, *args, **kwargs):
        job_filter = JobFilter(request.GET,queryset=self.get_queryset())
        paginator = Paginator(job_filter.qs,self.paginate_by)
        page_number = request.GET.get('page')
        jobs = paginator.get_page(page_number)
        tags =Tag.objects.all()
        categories = Category.objects.select_related('user')
        return render(request,self.template_name,{'jobs':jobs,'tags':tags,'categories':categories,'job_filter':job_filter})
    
    def get_queryset(self):
        queryset = Job.objects.filter(status="Open",deadline__gte=datetime.now()).select_related('category','user').prefetch_related('tags').order_by('-created')
        job_filter = JobFilter(self.request.GET, queryset=queryset)
        if 'latest' in self.request.GET:
            queryset = queryset.order_by('-created')

        return job_filter.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job_filter"] = JobFilter(self.request.GET,queryset=self.get_queryset())        
        # context['tags']=Tag.objects.all()
        # context['categories']=Category.objects.select_related('user')
        return context
    
class JobApplicationsListView(LoginRequiredMixin,ListView):
    model = Application
    context_object_name = 'applications'
    template_name = 'applications/job-applications.html'
    # paginate_by = 10
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        job = get_object_or_404(Job, slug=slug)
        return job.job_application.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']
        context['job'] = get_object_or_404(Job, slug=slug)
        # context['ratings']=
        return context
    
class ApplicationApprovalView(UpdateView):
    model = Application
    fields = ["status"]
    template_name_suffix = "_status_form"

    def form_valid(self, form):
        job = self.object.job
        new_status = form.cleaned_data["status"]
        if new_status == "Accepted":
            job.status = "Waiting"
            Application.objects.filter(job=job).exclude(pk=self.object.pk).update(
                status="Not Accepted", approved_canceled_time = datetime.now()
            )
            # sending email notification
            applicant_email =self.object.user.email
            # applicant_email ='victorobwaku@gmail.com'
            subject = 'Application Accepted'
            context ={
                'job':job,
                'application': self.object,
                'applicant':self.object.user
            }
            message = render_to_string('emails/application-approved.html',context)
           
            send_email_notification.delay(subject,message,applicant_email)
            
            # sending sms notification
           
            # use this
            # twilio_message = f"Congratulations! Your application for the job '{job.title}' has been accepted."  # Compose the message
                      
            # recipient_phone_number ='+245342323'
            # send_sms_notification.delay(twilio_message,recipient_phone_number)
            
        else:
            self.object.status = new_status
            self.approved_canceled_time = datetime.now()
        self.object.save()
        job.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse(
            "job-applications", kwargs={"slug": self.object.job.slug}
        
        )
class ApplicationCancelView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    fields = ["status"]
    # template_name_suffix = '_confirm_delete'
    
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
            job_owner_email =self.object.user.email
            # job_owner_email='victorobwaku@gmail.com'
            
            subject = 'Approved Application Cancelled'
            context ={
                'job':job,
                'application': self.object,
                'applicant':self.object.user
            }
            message = render_to_string('emails/cancel-accepted-application.html',context)           
            print(job_owner_email,job.title)
            send_email_notification.delay(subject,message,job_owner_email)
            
            # sending sms notification           
            # recipient_phone_number = "077899877"
            # twilio_message = f"Congratulations! Your application for the job '{job.title}' has been accepted."  # Compose the message
            # send_sms_notification.delay(twilio_message,recipient_phone_number)
        else:
            self.object.status = new_status
            self.object.approved_canceled_time= datetime.now()
        self.object.save()
        job.save()
        return super().form_valid(form)
    
    
    
    def get_success_url(self):
        return reverse_lazy('job-applications', kwargs={'slug': self.object.job.slug})
    

class JobDoneView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    fields = ["status"]
        
    def test_func(self):
        application = self.get_object()
        return self.request.user == application.job.user
    
    def form_valid(self, form):
        job = self.get_object().job
        new_status = form.cleaned_data["status"]
        if new_status == "Done":
            job.status = "Done"
            Application.objects.filter(job=job).exclude(pk=self.object.pk).update(status="Failed")
            
        else:
            self.get_object().status = new_status
            self.get_object().approved_canceled_time= datetime.now()
        self.get_object().save()
        job.save()
        return super().form_valid(form)    
    
    def get_success_url(self):
        return reverse_lazy('job-applications', kwargs={'slug': self.object.job.slug})
    

# def MakePaymentView(request,):
#         cl = MpesaClient()
#         # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
#         phone_number = '0714900634'
#         amount = 1
#         account_reference = 'Kazi-Yangu'
#         transaction_desc = 'Payment For job id 2345332435'
#         callback_url =  'https://api.darajambili.com/express-payment'
#         response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
#         print(response)
#         return HttpResponse(response)


class ApplicantRatingsViews(LoginRequiredMixin,CreateView):
    model = Rating 
    form_class = RatingForm
    template_name ='ratings/ratings.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        # slug = self.kwargs['profile_slug']
        context["user_profile"] = get_object_or_404(Profile,slug=self.kwargs['profile_slug'])
        context["application"]  =get_object_or_404(Application,uuid=self.kwargs['application_slug'])
        return context
    
    def form_valid(self, form):
        profile = get_object_or_404(Profile, slug=self.kwargs['profile_slug'])
        r = form.save(commit=False)        
        r.user = self.request.user
        r.profile = profile
        r.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy("jobs")
    
# def ApplicantRatings
# def initiate_stk_push(request):
#     access_token_responce = get_access_token(request)
#     if isinstance(access_token_responce,JsonResponse):
#         access_token = access_token_responce.content.decode("utf-8")
#         access_token_json = json.loads(access_token)
#         access_token=access_token_json.get("access_token")
#         if access_token:
#             amount = 1
#             phone = "254714900634"
#             process_request_url ="https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#             callback_url= 'https://kariukijames.com/pesa/callback.php'
#             passkey ="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
#             business_short_code ="174379"
#             timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#             password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()
#             party_a = phone
#             party_b = '254708374149'
#             account_reference = "Technical"
#             transaction_desc ="stkpush test"
#             stk_push_headers = {
#                 'Content-Type': 'application/json',
#                 'Authorization': 'Bearer ' + access_token
#             }
#             stk_push_payload ={
#                 'BusinessShortCode':business_short_code,
#                 'Password':password,
#                 "Timestamp":timestamp,    
#                 "TransactionType": "CustomerPayBillOnline",    
#                 "Amount": amount,    
#                 "PartyA":party_a,    
#                 "PartyB":business_short_code,    
#                 "PhoneNumber":party_a,    
#                 "CallBackURL": callback_url,   
#                 "AccountReference":account_reference,    
#                 "TransactionDesc":transaction_desc
#             }
#             try:
#                 response = requests.post(process_request_url,headers=stk_push_headers,json=stk_push_payload)
#                 response.raise_for_status()
#                  # Raise exception for non-2xx status codes
#                 response_data = response.json()
#                 checkout_request_id = response_data['CheckoutRequestID']
#                 response_code = response_data['ResponseCode']
#                 if response_code == '0':
#                     return JsonResponse({'CheckoutRequestID':checkout_request_id})
#                 else :
#                     return JsonResponse({'error':"STK push failed."})
#             except requests.exceptions.RequestException as e:
#                 return JsonResponse({'error':str(e)})
#         else: 
#             return JsonResponse({'error':'Access token not found.'})
#     else:
#         return JsonResponse({"error":'Failed to retrieve access token'})
# from .generateAccessToken import get_access_token

# class CheckoutView(TemplateView):
#     model = Job
#     template_name = "payments/checkout.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["job"] = get_object_or_404(Job, slug=self.kwargs.get('slug'))
#         return context
    

class ComplaintsCreateView(LoginRequiredMixin,CreateView):
    model = Complaints
    template_name = "jobs/complaints.html"
    form_class = ComplaintsForm
    success_url = reverse_lazy('jobs')
    def form_valid(self, form):
        f = form.save(commit=False)
        f.user = self.request.user
        slug = self.kwargs['slug']        
        f.job = Job.objects.get(slug =slug)
        f.save()
        return super(ComplaintsCreateView,self).form_valid(form)
    
