from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegistrationAPIView,
    LoginAPIView,
    UserProfileAPIView,
    LogoutAPIView
)

urlpatterns = [
    path('auth/register/', RegistrationAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/profile/', UserProfileAPIView.as_view(), name='profile'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]