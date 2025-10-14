from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
class IsSupport(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.client or request.user.is_superuser