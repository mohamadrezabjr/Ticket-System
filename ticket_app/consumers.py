import base64
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile

from ticket_app.serializers import MessageListSerializer
from ticket_app.models import Ticket, Message


class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.group_name = f'ticket_{self.ticket_id}'
        self.ticket = await self.get_ticket(self.ticket_id)

        if not self.ticket:
            await self.close(reason = "ticket_not_found")
        self.user = self.scope['user']
        # if not self.has_permission(self.user, self.ticket):
        #     self.close("permission_denied")
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
        await self.close()

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
        file = event['message'].get('file', None)
        filename = event['message'].get('filename', None)
        body = event['message'].get('body', None)
        if file :
            decoded = base64.b64decode(file)
            file = ContentFile(decoded, name=filename)
        message = await self.create_message(self.ticket, body, file)
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def create_message(self, ticket, body, file):
        message = Message.objects.create(ticket = ticket, body = body, file = file)
        return MessageListSerializer(message).data

    @database_sync_to_async
    def has_permission(self, user, ticket):
        if user == ticket.client or user.is_superuser or user.is_support:
            return True
        return False
    @database_sync_to_async
    def get_ticket(self, id):
        try:
            ticket = Ticket.objects.get(id=id)
        except Ticket.DoesNotExist:
            return None
        else :
            return ticket