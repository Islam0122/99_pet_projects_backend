from django.urls import path
from .views import LoginView, LogoutView,MyProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('profile/', MyProfileView.as_view({
        'get': 'list',
    }), name='profile'),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
