from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    LoginView,
    TokenRefreshViewCustom,
    LogoutView,
    ChangePasswordView,
    SendEmailView,
    UserViewSet,
    UserProfileViewSet
)

# Роутер для ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'profiles', UserProfileViewSet, basename='profiles')

urlpatterns = [
    # JWT Auth
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/token/refresh/', TokenRefreshViewCustom.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),

    # Change password
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),

    # Send email
    path('auth/send-email/', SendEmailView.as_view(), name='send_email'),

    # ViewSet через роутер
    path('', include(router.urls)),
]
