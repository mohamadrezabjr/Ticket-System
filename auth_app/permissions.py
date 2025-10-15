from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    message = 'permission denied, you are not the owner'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsAdmin(permissions.BasePermission):
    message = 'Permission denied, You are not an administrator'
    def has_permission(self, request, view):
        return request.user.is_superuser
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser

class IsSupport(permissions.BasePermission):
    message = 'Permission denied, You are not a Support'
    def has_permission(self, request, view):
        return request.user.is_support

class IsTicketOwner(permissions.BasePermission):
    message = 'permission denied, you are not the owner of this ticket'

    def has_object_permission(self, request, view, obj):
        return obj.client == request.user
class IsSupportOrAdmin(permissions.BasePermission):
    message = 'permission denied, you are not the admin or support'
    def has_permission(self, request, view):
        return request.user.is_support or request.user.is_superuser
    def has_object_permission(self, request, view, obj):
        return request.user.is_support or request.user.is_superuser

