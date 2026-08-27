import django_filters
from rest_framework import generics, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django.db.models import F, Count
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Tag, Post
from .serializers import CategorySerializer, TagSerializer, PostSerializer
from .pagination import BlogPagination
from permissions import IsOwnerOrReadOnly


class PostFilter(django_filters.FilterSet):
    """
    Maps the query params documented in the spec (?category=<slug>,
    ?tag=<slug>) onto the underlying FK/M2M slug lookups, instead of
    leaking Django's double-underscore field names into the public API.
    """
    category = django_filters.CharFilter(field_name='category__slug')
    tag = django_filters.CharFilter(field_name='tags__slug')

    class Meta:
        model = Post
        fields = ['category', 'tag', 'status', 'is_featured']

# How long (seconds) a single visitor's view of a single post counts only once.
# 24 hours means a visitor re-reading the same post the same day doesn't
# inflate views_count, but a genuine return visit the next day does count again.
VIEW_COOLDOWN_SECONDS = 60 * 60 * 24

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
    filterset_class = PostFilter
    search_fields = ['title', 'excerpt', 'content']
    # 'likes_count' works because get_queryset() annotates it below;
    # OrderingFilter can only sort by real DB columns/annotations, not by
    # a SerializerMethodField, so the annotation is required here.
    ordering_fields = ['published_at', 'views_count', 'likes_count', 'title']
    pagination_class = BlogPagination  # 6 per page, per spec B-18

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.annotate(likes_count=Count('likes', distinct=True))

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

        # Only count a view once per visitor per cooldown window, and never
        # count the owner's own visits (so editing/previewing a post doesn't
        # inflate its stats). Guarded with a cache key + F() update so we
        # never do a read-modify-save race.
        is_owner = request.user.is_authenticated and request.user.is_superuser
        if visitor_id and not is_owner:
            cache_key = f'post_view:{instance.id}:{visitor_id}'
            if cache.add(cache_key, True, timeout=VIEW_COOLDOWN_SECONDS):
                # cache.add() only succeeds if the key didn't already exist,
                # so this block runs at most once per visitor per cooldown.
                Post.objects.filter(id=instance.id).update(views_count=F('views_count') + 1)
                instance.refresh_from_db()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)