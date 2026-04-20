from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from accounts.views import RegisterView, ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/jwt/create/', TokenObtainPairView.as_view()),
    path('api/v1/auth/jwt/refresh/', TokenRefreshView.as_view()),
    path('api/v1/auth/register/', RegisterView.as_view()),
    path('api/v1/auth/me/', ProfileView.as_view()),
    path('api/', include('projects.urls')),
]