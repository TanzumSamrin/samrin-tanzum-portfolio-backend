from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Tag, Post
from .serializers import CategorySerializer, TagSerializer, PostSerializer
from permissions import IsOwnerOrReadOnly

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_destroy(self, instance):
        if instance.posts.filter(status='PUBLISHED').exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'detail': 'Cannot delete category with published posts.'})
        instance.delete()

class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsOwnerOrReadOnly]

class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsOwnerOrReadOnly]

class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category__slug', 'status', 'is_featured']
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['published_at', 'views_count', 'title']
    pagination_class = None  # We'll set this globally or here

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.all()
        
        # Owner can see all posts including drafts
        if user.is_authenticated and user.is_superuser:
            status = self.request.query_params.get('status')
            if status == 'DRAFT':
                queryset = queryset.filter(status='DRAFT')
            elif status == 'all':
                pass  # Show all
            else:
                queryset = queryset.filter(status='PUBLISHED')
        else:
            # Visitors only see published posts
            queryset = queryset.filter(status='PUBLISHED')
        
        return queryset

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_superuser:
            return Post.objects.all()
        return Post.objects.filter(status='PUBLISHED')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        visitor_id = request.headers.get('X-Visitor-Id')
        
        # Increment views only if visitor_id is present (prevent double counting)
        if visitor_id and request.method == 'GET':
            # Simple cooldown: use a session or cache to track views
            # For now, we'll increment using F() expression
            Post.objects.filter(id=instance.id).update(views_count=F('views_count') + 1)
            instance.refresh_from_db()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)