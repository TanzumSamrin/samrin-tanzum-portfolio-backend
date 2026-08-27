from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Comment
import os

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    """Send email notification when a new comment is created (console backend)"""
    if created and not instance.is_approved:
        subject = f"New comment awaiting approval on {instance.post.title}"
        message = f"""
        A new comment has been posted on your blog post "{instance.post.title}".
        
        Comment by: {instance.name}
        Email: {instance.email}
        Content: {instance.content[:200]}...
        
        Please review and approve it in the admin dashboard.
        """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])