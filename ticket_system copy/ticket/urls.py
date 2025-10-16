from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name = 'category-list-create'),
    path('categories/<int:category_id>/', CategoryDetailAPIView.as_view(), name = 'category-deatail')
]
