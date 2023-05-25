from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from .models import BlogWriter, Organization, Organizer, Player
import os
from django.db.models.signals import pre_delete

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


""" @receiver(pre_delete, sender=Player)
@receiver(pre_delete, sender=BlogWriter)
@receiver(pre_delete, sender=Organizer)
@receiver(pre_delete, sender=Organization)
def delete_profile_picture(sender, instance, **kwargs):
    if hasattr(instance, 'profile_picture') and instance.profile_picture:
        instance.profile_picture.delete(False) """