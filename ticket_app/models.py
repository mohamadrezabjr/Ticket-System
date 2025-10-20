from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TicketCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Ticket Categories'

    def __str__(self):
        return self.name

class Ticket(models.Model):
    class AdminStatus(models.TextChoices):
        NEW = 'N', 'جدید'
        ANSWERED = 'A', 'پاسخ داده شده'
        SEEN = 'S', 'دیده شده'
        CLOSED = 'C', 'بسته شده'

    class UserStatus(models.TextChoices):
        PENDING = 'P', 'در انتظار پاسخ'
        ANSWERED = 'A', 'پاسخ داده شده'
        CLOSED = 'C', 'بسته شده'
    class PriorityChoices(models.TextChoices):
        LOW = ('L', 'کم-جزئی')
        MEDIUM = ('M', 'متوسط-پیش‌فرض')
        HIGH = ('H', 'بالا-فوری')

    title = models.CharField(max_length=100,)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        TicketCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name = 'tickets',
    )
    user_status = models.CharField(
        choices=UserStatus.choices,
        max_length=10,
        default = UserStatus.PENDING
    )
    admin_status = models.CharField(
        choices=AdminStatus.choices ,
        max_length=10,
        default = AdminStatus.NEW
    )
    priority = models.CharField(
        choices=PriorityChoices.choices,
        max_length=10,
        default = PriorityChoices.MEDIUM,
    )
    client = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name = 'tickets',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_closed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_closed :
            self.admin_status = Ticket.AdminStatus.CLOSED
            self.user_status = Ticket.UserStatus.CLOSED
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.title} - {self.client}"


def message_upload_path(instance, filename):
    return f'files/ticket_{instance.ticket.id}/{instance.created_at.strftime('%Y-%m-%d %H:%M')}_{filename}'

class Message(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name = 'messages'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='messages'
    )
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(null=True, blank=True, upload_to=message_upload_path)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"پیام #{self.id} از {self.sender}"