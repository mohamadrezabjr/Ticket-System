from django.template.context_processors import request
from rest_framework import serializers, status
from admin_app.models import UserNotification
from .models import TicketCategory
from ticket_app.models import Ticket, Message
from ticket_app.models import TicketCategory
from ticket_system.serializers import UserInfoSerializer

class TicketSerializer(serializers.ModelSerializer):
    client = UserInfoSerializer(read_only=True)

    admin_status_display = serializers.CharField(source='get_admin_status_display', read_only=True)
    user_status_display = serializers.CharField(source='get_user_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset= TicketCategory.objects.all()
    )
    file = serializers.FileField(required=False)

    class Meta:
        model = Ticket
        fields = [
            'pk',
            'title',
            'description',
            'priority',
            'category',
            'client',
            'created_at',
            'updated_at',
            'priority_display',
            'admin_status_display',
            'user_status_display',
            'user_status',
            'admin_status',
            'is_closed',
            'file',
        ]
        read_only_fields = [
            'pk',
            'client',
            'created_at',
            'updated_at',
            'priority_display',
            'admin_status_display',
            'user_status_display',
            'user_status',
            'admin_status',
            'is_closed',
        ]

    def create(self, validated_data):
        try:
            file = validated_data.pop('file')
        except KeyError:
            file = None

        ticket = Ticket.objects.create(**validated_data)
        description = validated_data.get('description', None)
        message = Message.objects.create(ticket=ticket, body=description, file=file, sender = ticket.client)

        return ticket

class MessageListSerializer(serializers.ModelSerializer):
    sender = UserInfoSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'pk',
            'body',
            'sender',
            'file',
            'created_at',
        ]
class MessageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = [
            'pk',
            'ticket',
            'body',
            'sender',
            'file',
            'created_at',
        ]
        read_only_fields = [
            'pk',
            'sender',
            'ticket',
            'created_at',
        ]

    def create(self, validated_data):
        ticket = validated_data['ticket']
        sender = validated_data['sender']

        if ticket.is_closed:
            raise serializers.ValidationError({'error' :'Ticket is closed'}, status.HTTP_400_BAD_REQUEST)

        if sender.is_superuser or sender.is_support:
            ticket.admin_status = Ticket.AdminStatus.ANSWERED
            ticket.user_status = Ticket.UserStatus.ANSWERED
            ticket.save()
        else:
            ticket.admin_status = Ticket.AdminStatus.NEW
            ticket.user_status = Ticket.UserStatus.PENDING
            ticket.save()
        message = Message.objects.create(**validated_data)
        return message
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = '__all__'
class UserNotificationsSerializer(serializers.ModelSerializer):

    title = serializers.CharField(source='notification.title', read_only=True)
    category = serializers.CharField(source='notification.get_category_display', read_only=True)
    message = serializers.CharField(source='notification.message', read_only=True)
    class Meta:
        model = UserNotification
        fields = [
            'title',
            'category',
            'message',
            'is_read',
            'created_at',

        ]
        ordering = ('created_at',)