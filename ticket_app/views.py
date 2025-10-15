from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.permissions import IsAdmin, IsSupportOrAdmin, IsTicketOwner

from ticket_app.models import Ticket
from ticket_app.serializers import TicketSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        is_admin_or_support = self.request.user.is_superuser or self.request.user.is_support
        if user.is_authenticated and not is_admin_or_support:
            queryset = queryset.filter(client=user)
        return queryset

    def get_permissions(self):
        permission_map = {
            'retrieve': [IsAuthenticated, IsTicketOwner | IsSupportOrAdmin],
            'update': [IsAuthenticated, IsTicketOwner | IsSupportOrAdmin],
            'partial_update': [IsAuthenticated, IsTicketOwner | IsAdmin],
            'destroy': [IsAuthenticated, IsTicketOwner | IsAdmin],
        }
        default_permissions = [IsAuthenticated]
        permission_classes = permission_map.get(self.action, default_permissions)
        return [perm() for perm in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.user != instance.client and instance.admin_status == Ticket.AdminStatus.NEW :
            instance.admin_status = Ticket.AdminStatus.SEEN
            instance.save()
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)



