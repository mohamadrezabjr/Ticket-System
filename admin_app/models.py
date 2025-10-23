from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    class NotificationCategory(models.TextChoices):
        NEW_MESSAGE = 'N', 'پیام جدید از پشتیبانی'
        TICKET_CLOSE = 'C', 'بسته شدن تیکت'
        SYSTEM = 'S', 'اعلان سیستمی'
    title = models.CharField(max_length = 255, null = True, blank = True)
    category = models.CharField(max_length = 30, choices = NotificationCategory.choices, default = NotificationCategory.NEW_MESSAGE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self) -> str:
        return f'{self.get_category_display()}_{self.title}'

class UserNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete = models.CASCADE, related_name = 'user_notifications')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'notifications')
    is_read = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self) :
        return f'{str(self.notification)}_{self.user}'