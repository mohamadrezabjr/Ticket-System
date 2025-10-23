from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from auth_app.models import User
from auth_app.permissions import IsAdmin
from admin_app.models import Notification
from admin_app.serializers import NotificationSerializer, UserSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
