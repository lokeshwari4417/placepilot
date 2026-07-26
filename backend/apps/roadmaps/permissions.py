"""Custom permission classes for the 'roadmaps' module."""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow only the owner to edit, others can read."""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
