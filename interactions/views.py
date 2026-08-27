import uuid
from rest_framework import generics, permissions, status, filters
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from blog.models import Post
from .models import PostLike, Comment, ContactMessage
from .serializers import CommentSerializer, ContactMessageSerializer, PostLikeSerializer
from .pagination import ContactPagination, CommentPagination
from permissions import IsOwnerOrReadOnly, IsOwnerOnly


class LikeToggleView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'like'

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, status='PUBLISHED')
        visitor_id = request.headers.get('X-Visitor-Id')

        # Spec (B-16 / acceptance test) requires 400 when the header is
        # missing, not a silently-generated one-off UUID (which would make
        # the toggle useless, since the visitor could never "un-like").
        if not visitor_id:
            return Response(
                {'error': 'X-Visitor-Id header is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        like, created = PostLike.objects.get_or_create(
            post=post,
            visitor_id=visitor_id,
            defaults={'ip_address': self.get_client_ip(request)}
        )

        if created:
            liked = True
        else:
            like.delete()
            liked = False

        likes_count = post.likes.count()
        return Response({
            'liked': liked,
            'likes_count': likes_count
        })

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class CommentListCreateView(generics.ListCreateAPIView):
    """
    Public, per-post endpoint: GET returns only approved top-level comments
    (threaded replies nested by the serializer); POST creates a new comment
    pending approval. This is NOT the moderation queue — see
    CommentModerationListView below for that.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'comment'

    def get_queryset(self):
        post_slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=post_slug, status='PUBLISHED')
        return Comment.objects.filter(post=post, parent__isnull=True, is_approved=True)

    def perform_create(self, serializer):
        post_slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=post_slug, status='PUBLISHED')
        serializer.save(post=post, is_approved=False)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'message': 'Your comment is awaiting approval.',
            **response.data
        }, status=status.HTTP_201_CREATED)


class CommentModerationListView(generics.ListAPIView):
    """
    GET /api/comments/ — owner-only moderation queue across ALL posts.
    Supports ?is_approved=false and ?post=<slug> per spec.
    IsOwnerOnly (not IsOwnerOrReadOnly) because this queue contains
    unapproved comments and commenter emails that must never be public.
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOnly]
    pagination_class = CommentPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'is_approved': ['exact'],
        'post__slug': ['exact'],
    }
    ordering_fields = ['created_at']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        # Allow the documented ?post=<slug> param as an alias for post__slug.
        post_slug = self.request.query_params.get('post')
        if post_slug:
            queryset = queryset.filter(post__slug=post_slug)
        return queryset


class CommentModerationView(generics.RetrieveUpdateDestroyAPIView):
    """
    Owner-only detail endpoint: approve/unapprove or delete a single comment.
    IsOwnerOnly (not IsOwnerOrReadOnly) — a visitor must not be able to GET
    an individual comment by id before it's approved, or see its email.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOnly]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        is_approved = request.data.get('is_approved', None)
        if is_approved is not None:
            instance.is_approved = is_approved
            instance.save()
        return Response({'message': 'Comment updated successfully.'})


class ContactMessageListCreateView(generics.ListCreateAPIView):
    """
    POST /api/contact/ — public, throttled, creates a message.
    GET  /api/contact/ — owner-only inbox, paginated (10/page), filterable
                         by ?is_read=false.

    Previously these were two separate view classes both registered at the
    literal path 'contact/' in urls.py. Django's URL resolver matches the
    FIRST pattern for a given path regardless of HTTP method, so the GET
    view was completely unreachable (any request to /api/contact/ — GET or
    POST — hit CreateAPIView, and GET on a CreateAPIView is a 405). One
    view with per-method permissions is the correct fix.
    """
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer
    pagination_class = ContactPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [IsOwnerOnly()]

    def get_throttles(self):
        if self.request.method == 'POST':
            self.throttle_scope = 'contact'
            return [ScopedRateThrottle()]
        return []


class ContactMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsOwnerOnly]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        is_read = request.data.get('is_read', None)
        if is_read is not None:
            instance.is_read = is_read
            instance.save()
        return Response({'message': 'Message updated successfully.'})
