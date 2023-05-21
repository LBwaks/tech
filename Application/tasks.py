from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from twilio.rest  import Client 

@shared_task
def send_email_notification(subject,message,recepient_email):
    email = EmailMessage(subject,message,settings.DEFAULT_FROM_EMAIL,[recepient_email])
    email.content_subtype ='html'
    email.send()
@shared_task
def send_sms_notification(message,recipient_phone_number):
    twilio_client = Client(settings.TWILIO_ACCOUNT_SID,settings.TWILIO_AUTH_TOKEN)
    twilio_message = twilio_client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=recipient_phone_number
    )
    