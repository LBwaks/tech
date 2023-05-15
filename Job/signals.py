from django.conf import settings
from  django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from Job.consumers import NotificationConsumer

@receiver(post_save, sender=Job)
def send_notification_on_job_added(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = 'user-notifications'
        event ={
            'type':'job_added',
            'text':instance.id
        }
        async_to_sync(channel_layer.group_send)(group_name, event)
        # consumer = NotificationConsumer()
        # event = {
        #     'type': 'job_added',
        #     'text': str(instance.id)
        # }
        # consumer.job_added(event)