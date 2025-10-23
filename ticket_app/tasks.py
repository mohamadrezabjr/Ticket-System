import os

from celery import shared_task
from django.conf import settings
from django.core.files.storage import default_storage
from ticket_app.models import Ticket, Message, TicketCategory
from django.db import transaction
from django.contrib.auth import get_user_model
from django.core.files import File
from pathlib import Path
User = get_user_model()

@shared_task
def create_ticket_and_first_message(file_path, data):
    client_id = data.pop('client_id')
    client  = User.objects.get(id = client_id)

    category_id = data.pop('category')
    category = TicketCategory.objects.get(id = category_id)

    ticket = Ticket.objects.create(**data, category=category, client= client)
    try :
        with default_storage.open(file_path, 'rb') as f:
            file = File(f, name = Path(file_path).name)
            description = data.get('description', None)
            message = Message.objects.create(ticket=ticket, body=description, file=file, sender=ticket.client)

    finally:
        full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)