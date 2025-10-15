from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .import views

urlpatterns = [
    # Authicated 
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',views.UserRegisterAPIView.as_view()),
    path('logout/',views.UserLogoutAPIView.as_view()),
    # Profile
    path('profile/<int:user_id>/',views.UserProfileAPIView.as_view()),
    path('profile/update/<int:user_id>/',views.UpdateProfileAPIView.as_view()),
]