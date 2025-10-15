from rest_framework import permissions

class IsTicketOwner(permissions.BasePermission):
    message = 'permission denied, you are not the owner of this ticket'

    def has_object_permission(self, request, view, obj):
        return obj.client == request.user