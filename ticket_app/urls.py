from django.urls import path, include
from rest_framework import routers
from ticket_app import views

router = routers.DefaultRouter()
router.register('tickets', views.TicketViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('tickets/<int:ticket_id>/messages/', views.MessagesListCreateView.as_view(), name='messages'),
    path('ticket-categories/', views.CategoryListCreateAPIView.as_view(), name = 'category-list-create'),
    path('ticket-categories/<int:category_id>/',views.CategoryDetailAPIView.as_view(), name = 'category-detail'),
    path('ticket-categories/<int:category_id>/delete/', views.CategoryDeleteAPIView.as_view(), name='category-delete'),
    path('notifications/', views.UserNotificationsListAPIView.as_view(), name = 'user-notifications'),
    path('notifications/<int:notification_id>/',views.UserNotificationDetailAPIView.as_view(), name = 'user-notification-detail'),
    path('notifications/seen_all/', views.seen_all_notifications, name = 'seen-all-notifications'),
]