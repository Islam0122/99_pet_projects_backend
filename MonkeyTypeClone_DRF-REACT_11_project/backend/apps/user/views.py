from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer ,GoogleAuthSerializer
from .models import User
import requests
from django.conf import settings

# -------------------------
# Регистрация
# -------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer


# -------------------------
# Логин через JWT
# -------------------------
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

# -------------------------
# Обновление токена
# -------------------------
class TokenRefreshViewCustom(TokenRefreshView):
    pass


# -------------------------
# Google OAuth2 Login
# -------------------------
class GoogleLoginView(APIView):
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': email.split('@')[0], 'auth_type': 'google'}
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)
