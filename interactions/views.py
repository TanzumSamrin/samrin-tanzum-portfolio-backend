import uuid
from rest_framework import generics, permissions, status, throttling
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from django.shortcuts import get_object_or_404
from blog.models import Post
from .models import PostLike, Comment, ContactMessage
from .serializers import CommentSerializer, ContactMessageSerializer, PostLikeSerializer
from permissions import IsOwnerOrReadOnly

class LikeToggleView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'like'

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug, status='PUBLISHED')
        visitor_id = request.headers.get('X-Visitor-Id')
        
        if not visitor_id:
            visitor_id = str(uuid.uuid4())
        
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
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]
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

class CommentModerationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        is_approved = request.data.get('is_approved', None)
        if is_approved is not None:
            instance.is_approved = is_approved
            instance.save()
        return Response({'message': 'Comment updated successfully.'})

class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]
    throttle_scope = 'contact'

class ContactMessageListView(generics.ListAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_fields = ['is_read']

class ContactMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        is_read = request.data.get('is_read', None)
        if is_read is not None:
            instance.is_read = is_read
            instance.save()
        return Response({'message': 'Message updated successfully.'})