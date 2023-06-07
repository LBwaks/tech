from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from ckeditor.fields import RichTextField
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
# User = 
CATEGORY =[
    ('General','General'),
    ('Payments','Payments'),
    ('Job Application','Job Application'),
    ('Support','Support'),
    
]
# Create your models here.
class Contact(models.Model):
    """Model definition for Contact."""

    # TODO: Define fields here
    name = models.CharField(_("Name"), max_length=50)
    email = models.EmailField(_("Email"), max_length=254)
    subject = models.CharField(_("Subject"), max_length=50)
    message = models.TextField(_("Description"))
    created = models.DateTimeField( auto_now_add=True)

    class Meta:
        """Meta definition for Contact."""

        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        """Unicode representation of Contact."""
        return self.name

    # def save(self):
    #     """Save method for Contact."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Contact."""
        return reverse('contact')
    
class Faq(models.Model):
    """Model definition for Faq."""

    # TODO: Define fields here
    title = models.CharField(_("Title"), max_length=50)
    user = models.ForeignKey(User, related_name='faq_user', on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from ="title")
    category = models.CharField(_("Category"),choices=CATEGORY, max_length=50)
    content = RichTextField(_('Content'))
    created = models.DateTimeField( auto_now=False, auto_now_add=True)
    class Meta:
        """Meta definition for Faq."""

        verbose_name = 'Faq'
        verbose_name_plural = 'Faqs'

    def __str__(self):
        return self.title

    # def save(self):
    #     """Save method for Faq."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Faq."""
        return ('')

    # TODO: Define custom methods here
class Service(models.Model):
    """Model definition for Service."""

    # TODO: Define fields here
    title = models.CharField(_("Title"), max_length=50)
    user = models.ForeignKey(User, related_name='services_user', on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from ="title")   
    content = RichTextField(_('Content'))
    created = models.DateTimeField( auto_now=False, auto_now_add=True)
    class Meta:
        """Meta definition for Service."""

        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        """Unicode representation of Service."""
        return self.title

    # def save(self):
    #     """Save method for Service."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Service."""
        return ('')

    # TODO: Define custom methods here
