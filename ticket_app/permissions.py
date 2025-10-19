from rest_framework import permissions
from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsTicketOwner(permissions.BasePermission):
    message = 'permission denied, you are not the owner of this ticket'

    def has_object_permission(self, request, view, obj):
        return obj.client == request.user
    


class IsAdminOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            return True
        
        return bool(request.user.is_superuser)