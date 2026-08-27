from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superusers to edit objects.
    Safe methods (GET, HEAD, OPTIONS) are allowed for anyone.
    Write methods are only allowed for the owner (superuser).
    """
    
    def has_permission(self, request, view):
        # Safe methods are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write methods require authentication and superuser status
        return request.user and request.user.is_authenticated and request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        # Safe methods are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write methods require authentication and superuser status
        return request.user and request.user.is_authenticated and request.user.is_superuser


class IsOwnerOnly(permissions.BasePermission):
    """
    Require an authenticated superuser for EVERY method, including GET.

    Use this for anything that must stay fully invisible to visitors:
    dashboard stats, the contact inbox, and the comment-moderation queue
    (which contains unapproved comments and commenter emails).
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_superuser
        )