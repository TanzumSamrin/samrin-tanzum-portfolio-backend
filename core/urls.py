from django.urls import path
from .views import (
    ProfileDetailView, SkillListCreateView, SkillDetailView,
    ExperienceListCreateView, ExperienceDetailView,
    EducationListCreateView, EducationDetailView
)

urlpatterns = [
    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('skills/', SkillListCreateView.as_view(), name='skill-list'),
    path('skills/<int:pk>/', SkillDetailView.as_view(), name='skill-detail'),
    path('experiences/', ExperienceListCreateView.as_view(), name='experience-list'),
    path('experiences/<int:pk>/', ExperienceDetailView.as_view(), name='experience-detail'),
    path('education/', EducationListCreateView.as_view(), name='education-list'),
    path('education/<int:pk>/', EducationDetailView.as_view(), name='education-detail'),
]