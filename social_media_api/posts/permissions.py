from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow full access only to owners; read-only for others.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only for safe methods
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write: only owner
        return hasattr(obj, 'author') and obj.author == request.user
