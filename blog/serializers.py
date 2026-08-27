from rest_framework import serializers
from .models import Category, Tag, Post
from core.models import Skill

class CategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('slug', 'created_at', 'updated_at')

class TagSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('slug', 'created_at', 'updated_at')

class PostSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags_list = TagSerializer(source='tags', many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    is_liked = serializers.SerializerMethodField()
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('slug', 'views_count', 'reading_time', 'published_at', 'created_at', 'updated_at')

    def get_is_liked(self, obj):
        request = self.context.get('request')
        visitor_id = request.headers.get('X-Visitor-Id')
        if visitor_id and hasattr(obj, 'likes'):
            return obj.likes.filter(visitor_id=visitor_id).exists()
        return False

    def validate(self, data):
        if data.get('title') and len(data['title']) < 5:
            raise serializers.ValidationError({'title': 'Title must be at least 5 characters.'})
        if data.get('status') == 'PUBLISHED':
            if len(data.get('content', '')) < 100:
                raise serializers.ValidationError({'content': 'Content must be at least 100 characters.'})
            if not data.get('category'):
                raise serializers.ValidationError({'category': 'Category is required.'})
        return data