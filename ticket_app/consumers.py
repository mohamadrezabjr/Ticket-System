import base64
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile

from ticket_app.serializers import MessageListSerializer
from ticket_app.models import Ticket, Message
from ticket_app.tasks import send_admin_answered_notification

class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.group_name = f'ticket_{self.ticket_id}'
        self.ticket = await self.get_ticket(self.ticket_id)

        if not self.ticket:
            await self.close(reason = "ticket_not_found")
            return

        self.user = self.scope['user']
        if not self.user.is_authenticated:
            await self.close(reason = "user_not_authenticated")
            return 
        if not await self.has_permission(self.user, self.ticket):
            await self.close("permission_denied")
            return

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        file = text_data_json.get('file', None)
        filename = text_data_json.get('filename', None)
        body = text_data_json.get('body', None)
        if file :
            if len(file) > 14 * 1024 *1024 :
                await self.send(text_data=json.dumps({'error': 'File too large'}))
                return

        await self.channel_layer.group_send(
            self.group_name,
            {
            'type': 'message_receive',
            'message': {"body": body, "filename": filename, "file": file},
            }
        )
    async def message_receive(self, event):
        message = event['message']
        file = message.get('file', None)
        filename = message.get('filename', None)
        body = message.get('body', None)
        if file :
            try:
                decoded = base64.b64decode(file)
                file = ContentFile(decoded, name=filename)
            except(base64.binascii.Error, ValueError):
                file = None
        message = await self.create_message(self.ticket, body, file)
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def create_message(self, ticket, body, file):
        message = Message.objects.create(ticket = ticket, body = body, file = file, sender = self.user)
        if self.user.is_superuser or self.user.is_support:
            ticket.admin_status = Ticket.AdminStatus.ANSWERED
            ticket.user_status = Ticket.UserStatus.ANSWERED
            send_admin_answered_notification.delay(ticket.client.id, ticket.title)
            ticket.save()
        else:
            ticket.admin_status = Ticket.AdminStatus.NEW
            ticket.user_status = Ticket.UserStatus.PENDING
            ticket.save()
        return MessageListSerializer(message).data
    @database_sync_to_async
    def has_permission(self, user, ticket):
        if user == ticket.client or user.is_superuser or user.is_support:
            return True
        return False
    @database_sync_to_async
    def get_ticket(self, id):
        return Ticket.objects.filter(id=id).first()