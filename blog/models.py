from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from core.models import Skill

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=300)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='posts/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    published_at = models.DateTimeField(blank=True, null=True)
    views_count = models.IntegerField(default=0)
    reading_time = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Calculate reading time (~200 words per minute)
        word_count = len(self.content.split())
        self.reading_time = max(1, round(word_count / 200))
        
        # Auto-set published_at when status changes to PUBLISHED
        if self.status == 'PUBLISHED' and not self.published_at:
            self.published_at = models.DateTimeField(auto_now_add=True)
        
        super().save(*args, **kwargs)

    def clean(self):
        if len(self.title) < 5:
            raise ValidationError({'title': 'Title must be at least 5 characters.'})
        if self.status == 'PUBLISHED':
            if len(self.content) < 100:
                raise ValidationError({'content': 'Content must be at least 100 characters for published posts.'})
            if not self.category:
                raise ValidationError({'category': 'Category is required for published posts.'})

    def __str__(self):
        return self.title