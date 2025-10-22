from celery import shared_task
from django.contrib.auth import get_user_model
from admin_app.models import UserNotification, Notification

User = get_user_model()

@shared_task
def create_user_notifications(user_ids, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if user_ids == ['all']:
        user_list = User.objects.all()
    else:
        user_list = User.objects.filter(id__in=user_ids)

    for user in user_list:
        UserNotification.objects.create(user=user, notification=notification)