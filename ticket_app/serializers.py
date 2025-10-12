from rest_framework import serializers

from ticket_app.models import Ticket


class TicketSerializer(serializers.ModelSerializer):

    admin_status_display = serializers.SerializerMethodField()
    user_status_display = serializers.SerializerMethodField()
    priority_display = serializers.SerializerMethodField()

    def get_admin_status_display(self, obj):
        return obj.get_admin_status_display()
    def get_user_status_display(self, obj):
        return obj.get_user_status_display()
    def get_priority_display(self, obj):
        return obj.get_priority_display()

    class Meta:
        model = Ticket
        fields = [
            'pk',
            'title',
            'description',
            'user_status',
            'admin_status',
            'user_status_display',
            'admin_status_display',
            'priority',
            'priority_display',
            'category',
            'client',
            'created_at',
            'updated_at',
        ]