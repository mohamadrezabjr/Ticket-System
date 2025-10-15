from rest_framework import serializers

from ticket_app.models import Ticket, Message
from ticket_app.models import TicketCategory
from ticket_system.serializers import UserInfoSerializer

class TicketSerializer(serializers.ModelSerializer):

    admin_status_display = serializers.CharField(source='get_admin_status_display', read_only=True)
    user_status_display = serializers.CharField(source='get_user_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset= TicketCategory.objects.all()
    )

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
        ]
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
            'ticket',
            'created_at',
        ]

    def create(self, validated_data):
        ticket = validated_data['ticket']
        sender = validated_data['sender']
        if sender.is_superuser or sender.is_support:
            ticket.admin = Ticket.AdminStatus.ANSWERED
            ticket.user_status = Ticket.UserStatus.ANSWERED
            ticket.save()
        else:
            ticket.admin_status = Ticket.AdminStatus.NEW
            ticket.user_status = Ticket.UserStatus.PENDING
            ticket.save()
        message = Message.objects.create(**validated_data)
        return message