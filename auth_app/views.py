from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from auth_app.permissions import IsOwner
from .models import Profile , User
from .serializers import (
    UserRegisterSerializer , UserLogoutSerializer , UserProfileSerializer , UpdateProfileSerializer
)


class UserRegisterAPIView(APIView):

    """
        User Registration
    """

    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self , request):
        serializer_data = self.serializer_class(data = request.data)
        if serializer_data.is_valid():
            user = serializer_data.save()

            # create token custom
            refresh = RefreshToken.for_user(user)
            refresh["phone"] = user.phone
            refresh["is_superuser"] = user.is_superuser
            refresh["is_support"] = user.is_support
            refresh["is_user"] = user.is_user

            access = refresh.access_token
            access["phone"] = user.phone
            access["is_superuser"] = user.is_superuser
            access["is_support"] = user.is_support
            access["is_user"] = user.is_user

            return Response({
                'user': serializer_data.data,
                'token':{
                    'access-token':str(access),
                    'refresh-token':str(refresh)
                }
            },status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):
    """
        User Logout
    """

    serializer_class = UserLogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self , request):
        serializer_data = self.serializer_class(data = request.data)
        if serializer_data.is_valid():
            refresh = serializer_data.validated_data.get("refresh")
            RefreshToken(refresh).blacklist()
            return Response({'message':"refresh token deleted"},status=status.HTTP_200_OK)
        return Response({'message':'Token expired or invalid'} , status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(APIView):
    """
        User Profile
    """

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated , IsOwner]

    def get(self , request , user_id):
        profile = Profile.objects.get(user__id = user_id)
        self.check_object_permissions(request,profile)
        serializer_data = self.serializer_class(instance = profile)
        return Response(data = serializer_data.data , status = status.HTTP_200_OK)        

class UpdateProfileAPIView(APIView):

    """
        Updating profile
    """

    serializer_class = UpdateProfileSerializer
    permission_classes = [permissions.IsAuthenticated,IsOwner]

    def patch(self , request , user_id):

        profile = Profile.objects.get(user__id = user_id)
        self.check_object_permissions(request,profile)
        serializer_data = self.serializer_class(instance = profile , data=request.data, partial=True)

        if serializer_data.is_valid():
                serializer_data.save()
                return Response(data = serializer_data.data , status = status.HTTP_200_OK)
        return Response(serializer_data.errors , status=status.HTTP_400_BAD_REQUEST)

