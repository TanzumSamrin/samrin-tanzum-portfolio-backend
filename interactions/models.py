import uuid
from django.db import models
from django.core.exceptions import ValidationError
from blog.models import Post

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    visitor_id = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'visitor_id')

    def __str__(self):
        return f"{self.visitor_id} likes {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if len(self.name) < 2:
            raise ValidationError({'name': 'Name must be at least 2 characters.'})
        if len(self.content) < 5 or len(self.content) > 1000:
            raise ValidationError({'content': 'Content must be between 5 and 1000 characters.'})

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if len(self.message) < 10 or len(self.message) > 2000:
            raise ValidationError({'message': 'Message must be between 10 and 2000 characters.'})

    def __str__(self):
        return f"Message from {self.name}: {self.subject}"