from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_contact_email(name,from_email,subject,message):
    # try:
         context = {
            "name": name,
            "email": from_email,
            "subject": subject,
            "message": message,
         }
         text_content = render_to_string("emails/contact-email.html", context)
         html_content = render_to_string("emails/contact-email.html", context)

         mail = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=from_email,
            to=["victorobwaku@gmail.com"],
        )
         mail.attach_alternative(html_content, "text/html")
         mail.send(fail_silently=False)
         print('sent')
    # except Exception as e:
    #     # Handle the exception (e.g., log the error, display a message, etc.)
    #     print(f"Error occurred while sending email: {e}")
