from django.contrib import admin

from .models import (
    Education,
    Experience,
    Profile,
    Skill,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
    )

    search_fields = (
        "name",
        "email",
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "proficiency",
        "order",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "category",
    )

    ordering = (
        "order",
        "name",
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "position",
        "start_date",
        "end_date",
        "is_current",
    )

    list_filter = (
        "is_current",
    )

    search_fields = (
        "company",
        "position",
    )

    ordering = (
        "-start_date",
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = (
        "institution",
        "degree",
        "start_year",
        "end_year",
    )

    search_fields = (
        "institution",
        "degree",
        "field_of_study",
    )

    ordering = (
        "-start_year",
    )