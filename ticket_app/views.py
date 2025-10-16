from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.permissions import IsAdmin, IsSupportOrAdmin
from ticket_app.permissions import IsTicketOwner

from ticket_app.models import Ticket, Message
from ticket_app.serializers import TicketSerializer, MessageListSerializer, MessageCreateSerializer
from ticket_system.serializers import TicketInfoSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        is_admin_or_support = user.is_superuser or user.is_support
        if not is_admin_or_support:
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

class MessagesListCreateView(generics.ListCreateAPIView):

    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated,]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MessageCreateSerializer
        return MessageListSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        ticket_id = self.kwargs['ticket_id']
        self.ticket = get_object_or_404(Ticket, pk=ticket_id)
        user = self.request.user
        is_admin_or_support = user.is_superuser or user.is_support
        queryset = queryset.filter(ticket=self.ticket)

        if user == self.ticket.client or is_admin_or_support:
            return queryset
        raise PermissionDenied('You are not allowed to see this ticket')

    def list(self, request, *args, **kwargs):
        messages = self.get_queryset()
        serializer = self.get_serializer(messages, many=True)
        ticket_data = TicketInfoSerializer(self.ticket).data

        return Response(
            {
                "ticket_info":ticket_data,
                "messages": serializer.data,
            }
        )

    def perform_create(self, serializer):
        user = self.request.user
        ticket_id = self.kwargs['ticket_id']
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        is_admin_or_support = user.is_superuser or user.is_support
        if user == ticket.client or is_admin_or_support:
            serializer.save(sender=self.request.user, ticket=ticket)
        else:
            raise PermissionDenied('You are not allowed to send message on this ticket')


