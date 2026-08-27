from django.urls import path
from .views import (
    LikeToggleView,
    CommentListCreateView,
    CommentModerationListView,
    CommentModerationView,
    ContactMessageListCreateView,
    ContactMessageDetailView,
)

urlpatterns = [
    path('posts/<slug:slug>/like/', LikeToggleView.as_view(), name='like-toggle'),
    path('posts/<slug:slug>/comments/', CommentListCreateView.as_view(), name='comment-list'),

    # Moderation queue (owner-only list across all posts) MUST be registered
    # before the detail route in intent, though since they have different
    # path shapes ('comments/' vs 'comments/<pk>/') order doesn't actually
    # matter here — kept for readability.
    path('comments/', CommentModerationListView.as_view(), name='comment-moderation-list'),
    path('comments/<int:pk>/', CommentModerationView.as_view(), name='comment-moderation-detail'),

    # Single view handles both POST (public, throttled) and GET (owner-only,
    # paginated) at the same path — see ContactMessageListCreateView.
    path('contact/', ContactMessageListCreateView.as_view(), name='contact-list-create'),
    path('contact/<int:pk>/', ContactMessageDetailView.as_view(), name='contact-detail'),
]
