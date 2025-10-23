from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import generics, viewsets, status, serializers, filters
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from admin_app.models import UserNotification
from ticket_app.models import TicketCategory
from auth_app.permissions import IsAdmin, IsSupportOrAdmin
from ticket_app.permissions import IsTicketOwner
from ticket_app.serializers import CategorySerializer, UserNotificationsSerializer
from .permissions import IsAdminOrReadOnly

from ticket_app.models import Ticket, Message
from ticket_app.serializers import TicketSerializer, MessageListSerializer, MessageCreateSerializer
from ticket_system.serializers import TicketInfoSerializer

def is_admin_or_support(user):
    return user.is_superuser or user.is_support

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related('client__profile_user', 'category',).all()
    serializer_class = TicketSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['description', 'title']
    filterset_fields = ['priority','user_status']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if not is_admin_or_support(user):
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
        category = TicketCategory.objects.filter(name = serializer.validated_data['category']).first()
        if not category:
            raise NotFound(f'Ticket category "{serializer.validated_data['category']}" not found.')
        serializer.save(client_id=self.request.user.id, category=category.id)

class MessagesListCreateView(generics.ListCreateAPIView):

    queryset = Message.objects.select_related('ticket__category', 'sender__profile_user', 'ticket__client').all()
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
        try:
            self.ticket =Ticket.objects.select_related('category', 'client').get(id = ticket_id)
        except Ticket.DoesNotExist:
            self.ticket = None
            return Response({'message' : 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        user = self.request.user
        queryset = queryset.filter(ticket=self.ticket)

        if user == self.ticket.client or is_admin_or_support(user):
            return queryset
        raise PermissionDenied('You are not allowed to see this ticket')

    def list(self, request, *args, **kwargs):
        messages = self.get_queryset()
        serializer = self.get_serializer(messages, many=True)
        if self.ticket :
            ticket_data = TicketInfoSerializer(self.ticket).data
        else :
            return Response({'message' : 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            {
                "ticket_info":ticket_data,
                "messages": serializer.data,
            }
        )

    def perform_create(self, serializer):
        user = self.request.user
        ticket_id = self.kwargs['ticket_id']
        try:
            ticket =Ticket.objects.select_related('category', 'client').get(id = ticket_id)
        except Ticket.DoesNotExist:
            raise NotFound({'message' : 'Ticket not found'})

        if user == ticket.client or is_admin_or_support(user):
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

class UserNotificationsListAPIView(generics.ListAPIView):
    serializer_class = UserNotificationsSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserNotification.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class UserNotificationDetailAPIView(generics.RetrieveAPIView):
    serializer_class = UserNotificationsSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserNotification.objects.select_related('user', 'notification').all()
    lookup_field = 'id'
    lookup_url_kwarg = 'notification_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied('You are not allowed to see this Notification')
        instance.is_read = True
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)