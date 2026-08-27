from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    TagListCreateView, TagDetailView,
    PostListCreateView, PostDetailView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('tags/', TagListCreateView.as_view(), name='tag-list'),
    path('tags/<slug:slug>/', TagDetailView.as_view(), name='tag-detail'),
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
]