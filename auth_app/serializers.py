from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User , Profile , Cities , Provinces , valid_phone_ir


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['phone'] = user.phone
        token['is_superuser'] = user.is_superuser
        token['is_support'] = user.is_support
        token['is_user'] = user.is_user

        return token
    
class UserRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[valid_phone_ir])
    password = serializers.CharField(write_only = True)

    def validate_phone(self , value):
        if User.objects.filter(phone = value).exists():
            raise serializers.ValidationError("Phone number allready exist!!!")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)
    city = serializers.StringRelatedField(read_only = True)
    province = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = Profile
        fields = ('user','username','email','city','province','image')

class UpdateProfileSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(slug_field='name',queryset = Cities.objects.all())
    province = serializers.SlugRelatedField(slug_field='name',queryset = Provinces.objects.all())
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ('username','email','image','city','province','phone')

    def update(self, instance, validated_data):
        user = instance
        phone = validated_data.pop('phone',{})

        if phone:
            user.user.phone = phone
            user.user.save()
        return super().update(instance, validated_data)
    