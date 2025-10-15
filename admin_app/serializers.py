from rest_framework import serializers
from django.contrib.auth import  get_user_model
from .models import *

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_staff']

class NotificationSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required= True
    )
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at', 'user_id']
        read_only_fields = ['id', 'is_read', 'created_at']
        
    def create(self, validated_data):
        user = validated_data.pop('user_id')# اینجا pop مقدار user_id رو میگیرد و میریزد توی user و از دیکشنری حذف میکنه تا مقدار اضافی وارد Notification نشه
        if user is None:
            user = self.context['request'].user
        notification = Notification.objects.create(user=user, **validated_data)
        return notification
        
        