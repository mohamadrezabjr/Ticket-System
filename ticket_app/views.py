from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.permissions import IsAdmin
from ticket_app.models import Ticket
from ticket_app.serializers import TicketSerializer
from permissions import IsOwner

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and not user.is_superuser:
            queryset = queryset.filter(client=user)
        return queryset

    def get_permissions(self):
        permission_map = {
            'retrieve': [IsAuthenticated, IsOwner | IsAdmin],
            'update': [IsAuthenticated, IsOwner | IsAdmin],
            'partial_update': [IsAuthenticated, IsOwner | IsAdmin],
            'destroy': [IsAuthenticated, IsOwner | IsAdmin],
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

