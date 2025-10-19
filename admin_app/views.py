from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import *
from auth_app.models import Profile
from .models import *
from .serializers import *
# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login_user(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return Response({'message': 'ورود موفق ✅'})
        return Response({'error': 'نام کاربری یا رمز اشتباه است ⚠️'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail = False, methods = ['post'], permission_classes = [IsAuthenticated])
    def loguot_user(self, request):
        logout(request)
        return Response({'message': 'خروج موفق'})

class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_supperuser:
            return Notification.objects.all()
        return Notification.objects.filter(user = user)
    
    @action(detail = True, methods = ['get', 'post'], permission_classes = [IsAuthenticated])
    def read_user_notification(self, request, pk):
        notification = self.get_object()
        if notification.user != request.user:
            return Response({'error': 'شما اجازه تغییر این اعلان رو ندارین!!'}, status = status.HTTP_400_BAD_REQUEST)
        
        notification.is_read = True
        notification.save()
        
        return Response({'message': 'اعلان خوانده شد'})
