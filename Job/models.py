from django.db import models

from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from .choices import COUNTY, JOB_TYPE, SEEKER_TYPE
import hashlib
import random
import time
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    """Model definition for Category."""

    # TODO: Define fields here
    user = models.ForeignKey(
        User,
        related_name="job_category",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from="name")
    description = models.TextField(max_length=250)
    is_published = models.BooleanField(default=True)
    # objects = models.Manager()
    # publishedCategory =CategoryManager()
    is_featured = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Category."""

        verbose_name = "Category"
        verbose_name_plural = "Categorys"

    def my_slugify_function(self, content):
        return content.replace("_", "-").lower()

    def __str__(self):
        return self.name


class Job(models.Model):
    """Model definition for Job."""

    # TODO: Define fields here
    user = models.ForeignKey(User, verbose_name=_(""), on_delete=models.CASCADE)
    reference_id = models.CharField(_("reference_id"), unique=True)
    title = models.CharField(_("Title"), max_length=50)
    slug = AutoSlugField(populate_from="title")
    category = models.ForeignKey(Category, verbose_name=_(""), on_delete=models.CASCADE)
    tags = TaggableManager(_("Tags"))
    content = RichTextField(_("Description"))
    deadline = models.DateTimeField(
        _("Application Deadline"), auto_now=False, auto_now_add=False
    )
    job_end_time = models.DateTimeField(
        _("To be done time"), auto_now=False, auto_now_add=False
    )
    skills = RichTextField(_("Skills"))
    job_type = models.CharField(_("Job type"), choices=JOB_TYPE, max_length=50)
    seeker_type = models.CharField(_("Seeker Type"), choices=SEEKER_TYPE, max_length=50)
    positions = models.IntegerField(_("Available position"))

    county = models.CharField(_("County"), choices=COUNTY, max_length=50)
    location = models.CharField(_("Location/Town/City"), max_length=50)
    address = models.CharField(_("Address"), max_length=50)

    status = models.CharField(default="Open")
    is_featured = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Job."""

        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        """Unicode representation of Job."""
        return self.title

    def my_slugify_function(self, content):
        return content.replace("_", "-").lower()

    def save(self, *args, **kwargs):
        """Save method for Job."""
        if not self.reference_id:
            self.reference_id = self.generate_reference_id()
        super().save(*args, **kwargs)

    def generate_reference_id(self):
        timestamp = int(time.time() * 1000)  # Convert timestamp to milliseconds
        random_num = random.randint(100000, 999999)  # Generate random 6-digit number
        unique_id = f"{timestamp}{random_num}"
        hashed_id = hashlib.sha256(unique_id.encode()).hexdigest()[:10]
        return hashed_id

    def get_absolute_url(self):
        """Return absolute url for Job."""
        return reverse ("job-details",kwargs={"slug": self.slug})

    # TODO: Define custom methods here
class JobImage(models.Model):
    """Model definition for JobImage."""

    # TODO: Define fields here
    job = models.ForeignKey(Job, verbose_name=_(""), on_delete=models.CASCADE)
    image = models.ImageField(_("Job Images"), upload_to='job_images/', default='job_images/default_image.jpg', blank=True,null=True, max_length=None)
    created = models.DateTimeField( auto_now_add=True)

    class Meta:
        """Meta definition for JobImage."""

        verbose_name = 'JobImage'
        verbose_name_plural = 'JobImages'

    def __str__(self):
        """Unicode representation of JobImage."""
        return  f'{self.job.title}-{self.id}'
