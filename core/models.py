from django.db import models
from django.core.exceptions import ValidationError

class Profile(models.Model):
    full_name = models.CharField(max_length=255)
    headline = models.CharField(max_length=255)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    x_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    years_of_experience = models.IntegerField(default=0)
    is_available_for_hire = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk and Profile.objects.exists():
            raise ValidationError("Only one profile can exist.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile of {self.full_name}"

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('FRONTEND', 'Frontend'),
        ('BACKEND', 'Backend'),
        ('DATABASE', 'Database'),
        ('DEVOPS', 'DevOps'),
        ('TOOLS', 'Tools'),
        ('SOFT_SKILL', 'Soft Skill'),
    ]
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(default=50)
    icon = models.CharField(max_length=100, blank=True, null=True)
    display_order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not 1 <= self.proficiency <= 100:
            raise ValidationError({'proficiency': 'Must be between 1 and 100.'})

    def __str__(self):
        return self.name

class Experience(models.Model):
    EMPLOYMENT_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('INTERNSHIP', 'Internship'),
        ('FREELANCE', 'Freelance'),
        ('CONTRACT', 'Contract'),
    ]
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES)
    location = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    company_url = models.URLField(blank=True, null=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def clean(self):
        from datetime import date
        if self.start_date and self.start_date > date.today():
            raise ValidationError({'start_date': 'Start date cannot be in the future.'})
        if self.is_current and self.end_date:
            raise ValidationError({'end_date': 'End date must be empty for current position.'})
        if not self.is_current and not self.end_date:
            raise ValidationError({'end_date': 'End date is required for past positions.'})
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': 'End date must be after start date.'})

    def __str__(self):
        return f"{self.role} at {self.company}"

class Education(models.Model):
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_year = models.IntegerField()
    end_year = models.IntegerField(blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.degree} from {self.institution}"