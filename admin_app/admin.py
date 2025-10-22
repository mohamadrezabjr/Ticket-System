from django.contrib import admin
from admin_app.models import Notification, UserNotification

admin.site.register(Notification)
admin.site.register(UserNotification)