from rest_framework import generics, viewsets

from ticket_app.models import Ticket
from ticket_app.serializers import TicketSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


