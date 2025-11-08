# urls.py
from django.urls import path
from .views import SendOTPView, VerifyOTPView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]
