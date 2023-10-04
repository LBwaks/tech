from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from django.db.models import Avg,Count
from PIL import Image
from ckeditor.fields import RichTextField
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .choices import USER_TYPE,MY_GENDER,COUNTY,RATINGS
from phonenumber_field.modelfields import PhoneNumberField
from .validators import validate_file_size
ext_validator = FileExtensionValidator(['jpg', 'png', 'jpeg'])
cv_validator = FileExtensionValidator(['pdf'])


def validate_age(value):
    today = date.today()
    min_birth_date = today - timedelta(days=365 * 18)  # Minimum birth date for 18 years or older
    if value > min_birth_date:
        raise ValidationError("You must be 18 years or older to register.")

def user_profile_path(instance, filename):
    return 'users/profile/user_{0}/{1}'.format(instance.user.id, filename)


# Create your models here.
class Profile(models.Model):
    """Model definition for Profile."""

    # TODO: Define fields here
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    title =models.CharField(_("Job Title"), max_length=50,blank=True,null=True)
    firstname = models.CharField(_("Firstname"), max_length=50)
    lastname = models.CharField(_("Lastname"), max_length=50)
    user_type= models.CharField(_("User Type"), choices=USER_TYPE,max_length=50)
    id_passport = models.CharField(_("ID/Passport"), max_length=10, unique=True, validators=[MinLengthValidator(6)],null=True, blank=True)
    tell=PhoneNumberField(unique=True,null=True, blank=True)
    slug = models.UUIDField(default=uuid.uuid4, editable=False)
  
    gender = models.CharField(_("Gender"), choices=MY_GENDER, max_length=50)
    dob = models.DateField(_("Date Of Birth"),validators=[validate_age],null=True, blank=True)
    county= models.CharField(_("County"),choices=COUNTY, max_length=50)
    location = models.CharField(_("Location"), max_length=50)
    address =models.CharField(_("Address"), max_length=50)
    skills =models.CharField(_("Skills"), max_length=50)
    experience = models.IntegerField(_("Years of Experience"), default=0)
    bio = RichTextField()
    
    profile = models.ImageField(
        _("Profile Picture"),
        upload_to='profiles',
       
        default="profiles/default_profile.png",
        validators=[ext_validator,validate_file_size],
    )
    status = models.CharField(_("Status"),default='Active', max_length=50)
    is_suspended=models.BooleanField(_("Suspended") ,default=False)
    twitter = models.URLField(_("Twitter"), max_length=200, null=True, blank=True)
    facebook = models.URLField(_("Facebook"), max_length=200, null=True, blank=True)
    instagram = models.URLField(_("Instagram"), max_length=200, null=True, blank=True)
    website = models.URLField(_("Website"), max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    

    class Meta:
        """Meta definition for Profile."""

        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        """Unicode representation of Profile."""
        return f"{self.firstname} {self.lastname}"

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.profile.path)
    #     max_size = (300, 300)
    #     if img.height > max_size[0] or img.width > max_size[1]:
    #         img.thumbnail(max_size)
    #         img.save(self.profile.path)

    def get_absolute_url(self):
        return reverse("user-profile", kwargs={"slug": self.slug})

    @property
    def profile_url(self):
        if self.profile and hasattr(self.profile, "url"):
            return self.profile.url
    def averageview(self):
        rating = Rating.objects.filter(profile=self).aggregate(average=Avg('ratings'))
        # avg= 0
        # if rating['average'] is not None:
        #     avg = float(rating['average'])
        #     return avg
        avg= rating['average'] or 0
        return float(avg)
    
    def ratingsCounter(self):
        ratings =Rating.objects.filter(profile=self).aggregate(count = Count('id'))
        # cnt = 0
        # if ratings['count'] is not None:
        #             cnt = int(ratings['count'])
        #             return cnt
        cnt = ratings['count'] or 0
        return int(cnt)
        
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.user_profile.save()
   
   
def user_documents_path(instance, filename):
    return 'users/documents/user_{0}/{1}'.format(instance.user.id, filename)
 
class ProfileCV(models.Model):
    """Model definition for ProfileCV."""

    # TODO: Define fields here
    user =models.ForeignKey(User,  on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, related_name='profile_cv', on_delete=models.CASCADE)
    cv = models.FileField(upload_to=user_documents_path, blank=True, null=True,validators=[cv_validator,validate_file_size])
    created = models.DateTimeField( auto_now_add=True)
    class Meta:
        """Meta definition for ProfileCV."""

        verbose_name = 'ProfileCV'
        verbose_name_plural = 'ProfileCVs'

    def __str__(self):
        """Unicode representation of ProfileCV."""
        return f"{self.profile.firstname}-{self.id}"
        # return  f'{self.job.title}-{self.id}'

class Rating(models.Model):
    """Model definition for Rating."""

    # TODO: Define fields here
    user = models.ForeignKey(User, related_name="rater", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, related_name="user_ratee", on_delete=models.CASCADE)
    ratings = models.IntegerField(_("Ratings"),choices=RATINGS)
    reviews = models.TextField(_("Review"))
    created = models.DateTimeField( auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Rating."""

        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        """Unicode representation of Rating."""
        return str(self.ratings)
        # return f"Ratbrangs: {self.get_ratings_display()}"

    # def save(self):
    #     """Save method for Rating."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Rating."""
        return ('')

    # TODO: Define custom methods here

class Education(models.Model):
    """Model definition for Education."""

    # TODO: Define fields here
    user_profile = models.ForeignKey(Profile,related_name='user_education', verbose_name=_(""), on_delete=models.CASCADE)
    slug=models.UUIDField(default=uuid.uuid4, editable=False)
    course = models.CharField(_("Course"),max_length=256)
    institution = models.CharField(_("Institution"),max_length=256)
    description = models.TextField(_("Description"), null=True, blank=True, max_length=250)
    start_date = models.DateField(_("Start Date"), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_("End Date"), auto_now=False, auto_now_add=False ,null=True,blank=True)
    created = models.DateTimeField(_(""), auto_now=False, auto_now_add=True)
    class Meta:
        """Meta definition for Education."""

        verbose_name = 'Education'
        verbose_name_plural = 'Educations'

    def __str__(self):
        """Unicode representation of Education."""
        return self.course

    # def save(self):
    #     """Save method for Education."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Education."""
        return ('')

    # TODO: Define custom methods here
class Experience(models.Model):
    """Model definition for Experience."""

    # TODO: Define fields here
    user_profile = models.ForeignKey(Profile,related_name='user_experince', verbose_name=_(""), on_delete=models.CASCADE)
    slug=models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(_("Title"), max_length=150)
    employer = models.CharField(_("Employer"), max_length=50)
    description = models.TextField(_("Explain Your Role"),blank=True, null=True)
    start_date = models.DateField(_("Start Date"), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_("End Date"),null=True,blank=True, auto_now=False, auto_now_add=False)
    created = models.DateTimeField( auto_now_add=True)
    class Meta:
        """Meta definition for Experience."""

        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'

    def __str__(self):
        """Unicode representation of Experience."""
        return self.title

    # def save(self):
    #     """Save method for Experience."""
    #     pass

    def get_absolute_url(self):
        """Return absolute url for Experience."""
        return ('')

    # TODO: Define custom methods here
