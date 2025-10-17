from rest_framework import serializers
from django.contrib.auth import  get_user_model
from auth_app.models import Profile
from .models import Notification
from auth_app.models import User



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'email', 'username', 'image']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required = False)
    class Meta:
        model = User
        fields = ['id', 'phone', 'is_support', 'is_user', 'profile']
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('phone', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        if profile_data:
            Profile.objects.create(user = user, **validated_data)
        return user
    
    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.is_support = validated_data.get('is_support', instance.is_support)
        instance.is_user = validated_data.get('is_user', instance.is_user)
        instance.save()
        
        profile_data = validated_data.get('profile', None)
        if profile_data:
            profile = getattr(instance, 'profile', None)
            if profile:
                profile.email = profile_data.get('email', profile.email)
                profile.username = profile_data.get('username', profile.username)
                profile.image = profile_data.get('image', profile.image)
            else:
                Profile.objects.create(
                    user = instance,
                    email = profile_data.get('email', ''),
                    username = profile_data.get('username', ''),
                    image = profile_data.get('image', None)
                )
        return instance
        
        

class NotificationSerializer(serializers.ModelSerializer):
    user_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required= False, many = True
    )
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at', 'user_ids']
        read_only_fields = ['id', 'is_read', 'created_at']
        
    def create(self, validated_data):
        user_list  = validated_data.pop('user_ids', None)
        if user_list == 'all':
            user_list = User.objects.all()
            
        if user_list:
            notifications = []
            for item in user_list:
                notification = Notification.objects.create(user = item, **validated_data)
                notifications.append(notification)
            return notifications
        else:
            user = self.context['request'].user
            return Notification.objects.create(user = user, **validated_data)
            
        
        