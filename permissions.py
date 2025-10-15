from rest_framework.permissions import BasePermission , SAFE_METHODS


class IsOwner(BasePermission):
    message = 'permission denied, you are not the owner'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
        