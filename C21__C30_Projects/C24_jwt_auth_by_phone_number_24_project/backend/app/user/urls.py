from django.urls import path
from .views import (
    UserRegistrationView,
    UserProfileView,
    UserListView,
    ResendOTPView, OTPAuthenticationView  # Импортируем новый представление для повторной отправки OTP
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('otp/resend/', ResendOTPView.as_view(), name='otp-resend'),
    path('authenticate/', OTPAuthenticationView.as_view(), name='otp-authenticate'),

]