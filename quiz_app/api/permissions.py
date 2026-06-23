from rest_framework import permissions

class IsQuizOwner(permissions.BasePermission):
    """
    Custom permission class that restricts object access strictly to its owner.
    
    If validation fails, DRF automatically intercepts the request and raises
    an HTTP 403 Forbidden status accompanied by the German requirements message.
    """
    message = "Access denied - Quiz does not belong to the user."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user