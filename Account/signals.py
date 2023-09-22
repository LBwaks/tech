from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile  
from allauth.account.signals import user_logged_in


@receiver(user_logged_in)
def create_user_profile(sender, request, user, **kwargs):
    Profile.objects.get_or_create(user=user)
