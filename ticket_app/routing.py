from django.urls import path
from ticket_app.consumers import TicketConsumer

websocket_urlpatterns = [
    path("ws/ticket/<int:ticket_id>/", TicketConsumer.as_asgi(), name="ticket_consumer"),
]