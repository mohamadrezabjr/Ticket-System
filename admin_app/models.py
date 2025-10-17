from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationCategeory(models.TextChoices):
    info = 'اطلاع رسانی'
    warning = 'هشدار'
    promo = 'تبلیغات'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'notifications')
    title = models.CharField(max_length = 255)
    category = models.CharField(max_length = 30, choices = NotificationCategeory.choices, default = NotificationCategeory.info)
    message = models.TextField()
    is_read = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self) -> str:
        return self.user
    