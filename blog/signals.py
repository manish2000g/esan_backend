from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Article
import os

@receiver(pre_delete, sender=Article)
def delete_player_profile_picture(sender, instance, **kwargs):
    # Delete the profile picture file when a Player instance is deleted
    if instance.profile_picture:
        if os.path.isfile(instance.profile_picture.path):
            os.remove(instance.profile_picture.path)
