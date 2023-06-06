from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
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
