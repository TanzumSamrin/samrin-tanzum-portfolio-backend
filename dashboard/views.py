from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum, Q
from django.utils import timezone
from blog.models import Post, Category, Tag
from projects.models import Project
from core.models import Skill
from interactions.models import Comment, ContactMessage
from permissions import IsOwnerOrReadOnly

class DashboardStatsView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request):
        # Total counts
        total_posts = Post.objects.count()
        published_posts = Post.objects.filter(status='PUBLISHED').count()
        draft_posts = Post.objects.filter(status='DRAFT').count()
        total_projects = Project.objects.count()
        total_skills = Skill.objects.count()
        total_comments = Comment.objects.count()
        pending_comments = Comment.objects.filter(is_approved=False).count()
        total_likes = Sum('posts__likes')  # This needs to be calculated properly
        total_views = Post.objects.aggregate(Sum('views_count'))['views_count__sum'] or 0
        unread_messages = ContactMessage.objects.filter(is_read=False).count()

        # Top 5 posts by views
        top_posts = Post.objects.filter(status='PUBLISHED').order_by('-views_count')[:5].values(
            'title', 'slug', 'views_count'
        )
        # Annotate with likes_count
        top_posts = Post.objects.filter(status='PUBLISHED').order_by('-views_count')[:5].annotate(
            likes_count=Count('likes')
        ).values('title', 'slug', 'views_count', 'likes_count')

        # Recent comments (latest 5)
        recent_comments = Comment.objects.filter(is_approved=True).order_by('-created_at')[:5].values(
            'name', 'content', 'post__title', 'created_at'
        )

        # Posts per month (last 6 months)
        from django.db.models.functions import TruncMonth
        posts_per_month = Post.objects.filter(
            status='PUBLISHED',
            published_at__gte=timezone.now() - timezone.timedelta(days=180)
        ).annotate(
            month=TruncMonth('published_at')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')

        return Response({
            'total_posts': total_posts,
            'published_posts': published_posts,
            'draft_posts': draft_posts,
            'total_projects': total_projects,
            'total_skills': total_skills,
            'total_comments': total_comments,
            'pending_comments': pending_comments,
            'total_views': total_views,
            'unread_messages': unread_messages,
            'top_posts': top_posts,
            'recent_comments': recent_comments,
            'posts_per_month': posts_per_month,
        })