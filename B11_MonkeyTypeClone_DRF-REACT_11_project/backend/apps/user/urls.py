from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, TokenRefreshViewCustom, GoogleLoginView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshViewCustom.as_view(), name="token_refresh"),
    path("google/", GoogleLoginView.as_view(), name="google_login"),

]
