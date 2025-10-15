from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ticket_app.urls')),
    path('auth/', include('auth_app.urls')),
    path('admin_app/', include('admin_app.urls')),
]
