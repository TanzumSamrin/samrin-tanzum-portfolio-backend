from django.urls import path
from .views import (
    LikeToggleView, CommentListCreateView, CommentModerationView,
    ContactMessageCreateView, ContactMessageListView, ContactMessageDetailView
)

urlpatterns = [
    path('posts/<slug:slug>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('posts/<slug:slug>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentModerationView.as_view(), name='comment-moderation'),
    path('contact/', ContactMessageCreateView.as_view(), name='contact-create'),
    path('contact/', ContactMessageListView.as_view(), name='contact-list'),
    path('contact/<int:pk>/', ContactMessageDetailView.as_view(), name='contact-detail'),
]