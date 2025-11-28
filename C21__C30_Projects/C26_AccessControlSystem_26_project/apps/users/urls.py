from django.urls import path
from .views import (
    RegisterView,
    VerifyOtpView,
    LoginView,
    logout_view,
    profile_view,
    UpdateProfileView,
    SoftDeleteView,
    test_protected_view
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', profile_view, name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='profile-update'),
    path('profile/delete/', SoftDeleteView.as_view(), name='profile-delete'),

    path('protected/', test_protected_view, name='protected'),
]