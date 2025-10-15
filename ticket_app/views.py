from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.permissions import IsAdmin, IsSupportOrAdmin, IsTicketOwner

from ticket_app.models import Ticket, Message
from ticket_app.serializers import TicketSerializer, MessageListSerializer
from ticket_system.serializers import TicketInfoSerializer

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

class MessagesList(generics.ListAPIView):

    queryset = Message.objects.all()
    serializer_class = MessageListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        ticket_id = self.kwargs['ticket_id']
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        user = self.request.user
        is_admin_or_support = user.is_superuser or user.is_support
        queryset = queryset.filter(ticket=ticket)

        if user == ticket.client or is_admin_or_support:
            return queryset
        raise PermissionDenied('You are not allowed to see this ticket')
    def list(self, request, *args, **kwargs):
        messages = self.get_queryset()
        ticket_id = self.kwargs['ticket_id']
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        serializer = self.get_serializer(messages, many=True)
        ticket_data = TicketInfoSerializer(ticket).data

        return Response(
            {
                "ticket_info":ticket_data,
                "messages": serializer.data,
            }
        )

