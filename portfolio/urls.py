from django.urls import path

from .views import (
    EducationDetailAPIView,
    EducationListCreateAPIView,
    ExperienceDetailAPIView,
    ExperienceListCreateAPIView,
    ProfileAPIView,
    SkillDetailAPIView,
    SkillListCreateAPIView,
)


urlpatterns = [
    path("profile/", ProfileAPIView.as_view(), name="profile"),

    path("skills/", SkillListCreateAPIView.as_view(), name="skill-list"),
    path("skills/<int:pk>/", SkillDetailAPIView.as_view(), name="skill-detail"),

    path("experiences/", ExperienceListCreateAPIView.as_view(), name="experience-list"),
    path("experiences/<int:pk>/", ExperienceDetailAPIView.as_view(), name="experience-detail"),

    path("education/", EducationListCreateAPIView.as_view(), name="education-list"),
    path("education/<int:pk>/", EducationDetailAPIView.as_view(), name="education-detail"),
]