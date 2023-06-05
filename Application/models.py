from django.db import models
from ckeditor.fields import RichTextField
import uuid
from Job.models import Job
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext as _
# Create your models here.
class Application(models.Model):
    """Model definition for Application."""

    # TODO: Define fields here
    uuid = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    user = models.ForeignKey(User,related_name='user_application', on_delete=models.CASCADE,db_index=True)
    job = models.ForeignKey(Job, related_name='job_application', on_delete=models.CASCADE,db_index=True)
    charge = models.IntegerField(_("Fees"))    
    description = RichTextField()
    status = models.CharField(default='Pending', max_length=50, db_index=True)
    approved_canceled_time= models.DateTimeField(_("Approved / Rejected time"), blank=True,null=True,auto_now=False, auto_now_add=False)
    created = models.DateTimeField( auto_now_add=True)

    class Meta:
        """Meta definition for Application."""

        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering =['-approved_canceled_time']

    def __str__(self):
        """Unicode representation of Application."""
        return self.charge

    # def save(self):
    #     """Save method for Application."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Application."""
        return reverse ('application-details', kwargs={'slug': self.object.uuid})

    # TODO: Define custom methods here
