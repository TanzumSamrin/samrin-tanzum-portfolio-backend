from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list'),
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project-detail'),
]