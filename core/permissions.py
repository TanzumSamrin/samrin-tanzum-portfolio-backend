from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Allow read-only access to everyone.

    Allow write access only to authenticated superusers.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )


class IsOwnerOnly(BasePermission):
    """
    Require an authenticated superuser for EVERY method, including GET.

    Use this (never IsOwnerOrReadOnly) for anything that must stay fully
    invisible to visitors: dashboard stats, the contact inbox, and the
    comment-moderation queue (which contains unapproved comments + emails).
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )