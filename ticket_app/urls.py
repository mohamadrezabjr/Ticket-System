from django.urls import path, include
from rest_framework import routers
from ticket_app import views

router = routers.DefaultRouter()
router.register('tickets', views.TicketViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('tickets/<int:ticket_id>/messages/', views.MessagesListCreateView.as_view(), name='messages'),
]