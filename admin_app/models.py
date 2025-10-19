from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationCategeory(models.TextChoices):
    NEW_MESSAGE = 'N', 'پیام جدید از پشتیبانی'
    TICKET_CLOSE = 'C', 'بسته شدن تیکت'
    SYSTEM = 'S', 'اعلان سیستمی'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'notifications')
    title = models.CharField(max_length = 255, null = True, blank = True)
    category = models.CharField(max_length = 30, choices = NotificationCategeory.choices, default = NotificationCategeory.NEW_MESSAGE)
    message = models.TextField()
    is_read = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self) -> str:
        return f'{self.get_category_display()} برای {self.user.phone}'
    