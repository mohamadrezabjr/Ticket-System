from rest_framework import serializers
# from django.contrib.auth import  get_user_model
from .models import Notification
from auth_app.models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(required = False)    
    email = serializers.CharField(write_only=True, required=False, allow_blank=True)
    username = serializers.CharField(write_only=True, required=False, allow_blank=True)
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'phone', 'password', 'role', 'email', 'username', 'image']


    def get_role(self, obj):
        if getattr(obj, 'is_support', False):
            return "support"
        elif getattr(obj, 'is_user', False):
            return "user"
        return None

    def create(self, validated_data):
        role = validated_data.pop('role', None)
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)
        username = validated_data.pop('username', None)
        image = validated_data.pop('image', None)

        user = User.objects.create(**validated_data)

        if role == 'support':
            user.is_support = True
            user.is_user = False
        elif role == 'user':
            user.is_user = True
            user.is_support = False
        else:
            raise serializers.ValidationError({'role': 'Role must be "support" or "user".'})
        user.save()
    

        if password:
            user.set_password(password)
        user.save()

        (profile, created) = Profile.objects.get_or_create(user = user)
        if email:
            profile.email = email
        if username:
            profile.username = username
        if image:
            profile.image = image
        profile.save()

        return user
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_support:
            data['role'] = "support"
        elif instance.is_user:
            data['role'] = "user"
        else:
            data['role'] = None
        profile = Profile.objects.filter(user = instance).first()
        data['email'] = profile.email if profile else None
        data['username'] = profile.username if profile else None
        data['image'] = profile.image.url if profile and profile.image else None
        return data
    
    def update(self, instance, validated_data):
        role = validated_data.get('role', 'None')
        if role == 'support':
            instance.is_support = True
            instance.is_user = False
        elif role == 'user':
            instance.is_user = True
            instance.is_support = False
        
        phone = validated_data.get('phone', None)
        if phone:
            instance.phone = phone
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
            
        profile = getattr(instance, 'profile_user', None)
        profile.email = validated_data.get('email', profile.email)
        profile.username = validated_data.get('username', profile.username)
        profile.image = validated_data.get('image', profile.image)
        profile.save()
        
        return instance
        
        
    
class NotificationSerializer(serializers.ModelSerializer):
    user_ids = serializers.ListField(allow_empty=False, write_only=True)
    category_display = serializers.CharField(required=False, source='get_category_display')

    def to_internal_value(self, data):
        if isinstance(data.get('user_ids'), str):
            data['user_ids'] = [data['user_ids']]
        return super().to_internal_value(data)

    class Meta:
        model = Notification
        fields = ['id', 'title','category','category_display', 'message', 'is_read', 'created_at', 'user_ids']
        read_only_fields = ['id', 'category_display','is_read', 'created_at']
        
    def create(self, validated_data):
        user_ids  = validated_data.pop('user_ids', None)
        if user_ids == ['all']:
            user_list = User.objects.all()
        else :
            user_list = User.objects.filter(id__in=user_ids)

        for item in user_list:
            notification = Notification.objects.create(user = item, **validated_data)

        user = self.context['request'].user
        notification = Notification.objects.create(user = user, **validated_data)
        return notification
            
        
        
            
        
        