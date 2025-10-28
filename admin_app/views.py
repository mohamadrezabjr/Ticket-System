from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from auth_app.models import User
from auth_app.permissions import IsAdmin
from admin_app.models import Notification
from admin_app.serializers import NotificationSerializer, UserSerializer, UserResponseSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    @extend_schema(responses=UserResponseSerializer)
    def list(self, request, *args, **kwargs):
        return super(UserViewSet, self).list(request, *args, **kwargs)
    @extend_schema(responses=UserResponseSerializer)
    def retrieve(self, request, *args, **kwargs):
        return super(UserViewSet, self).retrieve(request, *args, **kwargs)
    @extend_schema(responses=UserResponseSerializer)
    def update(self, request, *args, **kwargs):
        return super(UserViewSet, self).update(request, *args, **kwargs)
    @extend_schema(responses=UserResponseSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super(UserViewSet, self).partial_update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user:
            return Response({"detail": "You can't delete yourself!"}, status=status.HTTP_403_FORBIDDEN)
        if instance.is_superuser:
            return Response({'detail': "You can't delete a superuser!"}, status=status.HTTP_403_FORBIDDEN)
        return super(UserViewSet, self).destroy(request, *args, **kwargs)
class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
