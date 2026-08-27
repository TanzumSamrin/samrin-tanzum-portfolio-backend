from django.core.exceptions import ValidationError
from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=150)
    headline = models.CharField(max_length=255)
    bio = models.TextField()

    location = models.CharField(max_length=150)
    email = models.EmailField()

    profile_image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True,
    )

    resume = models.FileField(
        upload_to="resume/",
        blank=True,
        null=True,
    )

    github_url = models.URLField(
        blank=True,
        null=True,
    )

    linkedin_url = models.URLField(
        blank=True,
        null=True,
    )

    website_url = models.URLField(
        blank=True,
        null=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def clean(self):
        if not self.pk and Profile.objects.exists():
            raise ValidationError(
                "Only one profile is allowed."
            )

    def __str__(self):
        return self.name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("database", "Database"),
        ("tools", "Tools"),
        ("other", "Other"),
    ]

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    proficiency = models.PositiveSmallIntegerField(
        default=0,
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="other",
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Experience(models.Model):
    company = models.CharField(
        max_length=200,
    )

    position = models.CharField(
        max_length=200,
    )

    start_date = models.DateField()

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    is_current = models.BooleanField(
        default=False,
    )

    description = models.TextField()

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.position} at {self.company}"


class Education(models.Model):
    institution = models.CharField(
        max_length=255,
    )

    degree = models.CharField(
        max_length=255,
    )

    field_of_study = models.CharField(
        max_length=255,
        blank=True,
    )

    start_year = models.PositiveIntegerField()

    end_year = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    grade = models.CharField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ["order", "-start_year"]

    def __str__(self):
        return (
            f"{self.degree} - "
            f"{self.institution}"
        )