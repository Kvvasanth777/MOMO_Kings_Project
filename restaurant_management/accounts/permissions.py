from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_staff:
            return True

        # Check if the object belongs to the request user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
