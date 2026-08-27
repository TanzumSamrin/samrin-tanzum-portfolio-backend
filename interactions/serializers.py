from rest_framework import serializers
from .models import PostLike, Comment, ContactMessage
from blog.models import Post

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['post', 'visitor_id']
        read_only_fields = ['visitor_id']

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'name', 'email', 'website', 'content', 'parent', 'replies', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_replies(self, obj):
        if obj.parent is None:
            replies = Comment.objects.filter(parent=obj, is_approved=True)
            return CommentSerializer(replies, many=True).data
        return []

    def validate(self, data):
        if data.get('name') and len(data['name']) < 2:
            raise serializers.ValidationError({'name': 'Name must be at least 2 characters.'})
        if data.get('content'):
            if len(data['content']) < 5 or len(data['content']) > 1000:
                raise serializers.ValidationError({'content': 'Content must be between 5 and 1000 characters.'})
        return data

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at', 'is_read']

    def validate(self, data):
        if data.get('message') and (len(data['message']) < 10 or len(data['message']) > 2000):
            raise serializers.ValidationError({'message': 'Message must be between 10 and 2000 characters.'})
        return data