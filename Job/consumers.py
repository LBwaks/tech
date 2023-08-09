from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import get_template
from channels.exceptions import StopConsumer
class NotificationConsumer(WebsocketConsumer):
     def connect(self):
        # self.user = self.scope['user']
        # if not self.user.is_authenticated:
        #      self.close()
        #      return
        self.GROUP_NAME = 'user-notifications'
        
        # Join room group
        if self.channel_layer is not None:
            async_to_sync(self.channel_layer.group_add)(
                self.GROUP_NAME, self.channel_name
            )
        self.accept()

     def disconnect(self, close_code):
        if self.channel_layer is not None:
            # if self.user.is_authenticated:
                async_to_sync(self.channel_layer.group_discard)(
                    self.GROUP_NAME, self.channel_name
                )
        raise StopConsumer()
    
     def job_added(self,event):
       
        html= get_template('includes/partials/notifications.html').render(
            context={'id':event['text']}
        )
        job_id = event['text'] 
        # # Implement your logic to fetch the job details using the job_id
        # # Send the job details as a WebSocket message to the connected users
        # self.send(text_data='A new job has been added with ID: {}'.format(job_id))
        self.send(text_data=html)
