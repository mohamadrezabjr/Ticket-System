from rest_framework.decorators import action
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import TicketCategory
from auth_app.permissions import IsAdmin, IsSupportOrAdmin
from ticket_app.permissions import IsTicketOwner
from .serializers import CategorySerializer
from .permissions import IsAdminOrReadOnly

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
            'partial_update': [IsAuthenticated, IsTicketOwner | IsSupportOrAdmin],
            'destroy': [IsAuthenticated, IsAdmin],
        }
        default_permissions = [IsAuthenticated]
        permission_classes = permission_map.get(self.action, default_permissions)
        return [perm() for perm in permission_classes]

    def get_object(self):
        obj = get_object_or_404(Ticket, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.user != instance.client and instance.admin_status == Ticket.AdminStatus.NEW :
            Ticket.objects.filter(id = instance.id).update(admin_status =Ticket.AdminStatus.SEEN)
        return Response(serializer.data)

    @action(detail = True, methods=['post', 'get'], permission_classes=[IsTicketOwner, IsSupportOrAdmin])
    def close(self, request, pk=None):
        instance = self.get_object()
        instance.is_closed = True
        instance.save()
        return Response({'message' : f'Ticket #{instance.id} successfully closed.'}, status=status.HTTP_200_OK)

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


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = TicketCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = TicketCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'category_id'
