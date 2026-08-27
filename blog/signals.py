from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Post
import os

@receiver(post_delete, sender=Post)
def delete_post_cover_image(sender, instance, **kwargs):
    """Delete cover image file when post is deleted"""
    if instance.cover_image:
        if os.path.isfile(instance.cover_image.path):
            os.remove(instance.cover_image.path)