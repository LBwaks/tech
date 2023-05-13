from django.conf import settings
from  django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@receiver(post_save ,sender =Job)
def send_notification_on_job_added(sender,created,instance,**kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = 'user-notifications'
        event ={
            'type':'job_added',
            'text':instance.id
        }
        async_to_sync(channel_layer.group_send)(group_name, event)