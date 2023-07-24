from django.shortcuts import render,redirect
from .forms import EmailForm
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib import messages
from mailchimp_marketing import Client
from django.conf import settings
from mailchimp_marketing.api_client import ApiClientError
import logging
logger = logging.getLogger(__name__)
import hashlib
# Create your views here.

mailchimp = Client()
mailchimp.set_config({
    'api_key':settings.MAILCHIMP_API_KEY,
    'server':settings.MAILCHIMP_REGION,
})

def subscribe (request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                form_email = form.cleaned_data['email']
                member_info={
                    'email_address':form_email,
                    'status':'subscribed',
                }
                response = mailchimp.lists.add_list_member(
                    settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                    member_info,
                )
                logger.info(f'API call successful: {response}')
                messages.success(request,'Subscription To Our Newsletter Successfull !')
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            
            except ApiClientError as error:
                
                logger.error(f'An exception occurred :{error.text}')
                messages.error(request,'Failed To Subscribe To Our Newsletter Try Again !')
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            
    return render(request,"pages/home.html" ,{'form':EmailForm()})

def mailchimp_ping_view(request):
    response = mailchimp.ping.get()
    return JsonResponse(response)


def unsubscribe(request):
    if request.method == "POST":
        form= EmailForm(request.POST)
        if form.is_valid():
            try:
                form_email = form.cleaned_data['email']
                form_email_hash= hashlib.md5(form_email.encode('utf-8').lower()).hexdigest()
                member_update ={
                    'status':'unsubscribed',
                }
                response = mailchimp.lists.update_list_member(
                    settings.MAILCHIMP_MARKETING_AUDIENCE_ID,
                    form_email_hash,
                    member_update
                )
                logger.info(f'API call successful: {response}')
                messages.success(request,'Unsubscription To Our Newsletter Successfull !')
                return redirect('home')
            
            except ApiClientError as error:
                
                logger.error(f'An exception occurred :{error.text}')
                messages.error(request,'Failed To Unsubscribe To Our Newsletter Try Again !')
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            
    return render(request,"pages/unsubscribe.html" ,{'form':EmailForm()})

          