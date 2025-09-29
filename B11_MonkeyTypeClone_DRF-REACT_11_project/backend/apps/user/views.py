from rest_framework import generics, status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer ,GoogleAuthSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from google.oauth2 import id_token
from google.auth.transport import requests

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
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "token": {"type": "string", "example": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE2..."}
                },
                "required": ["token"]
            }
        },
        responses={
            200: OpenApiResponse(
                description="Успешный вход через Google",
                response=UserSerializer
            ),
            400: OpenApiResponse(description="Ошибка авторизации"),
        },
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={"token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE2..."},
                request_only=True
            )
        ]
    )
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)

        CLIENT_ID = "472858064873-2ldpc5il9rils2dt9nq3uk5ddetrb1ft.apps.googleusercontent.com"
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

            email = idinfo.get("email")
            name = idinfo.get("name") or email.split("@")[0]

            user, created = User.objects.get_or_create(
                email=email,
                defaults={"username": name, "auth_type": "google"}
            )

            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
