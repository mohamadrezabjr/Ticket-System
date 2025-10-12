from django.contrib import admin
from ticket_app.models import *

admin.site.register(TicketCategory)
admin.site.register(Ticket)
admin.site.register(Message)

# Register your models here.
