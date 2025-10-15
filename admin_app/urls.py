from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename = 'users')
router.register('notifications', views.NotificationViewSet, basename = 'notification')

urlpatterns = router.urls


