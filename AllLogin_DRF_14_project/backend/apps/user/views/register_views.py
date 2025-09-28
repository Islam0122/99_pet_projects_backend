from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from ..serializers import UserRegisterSerializer, ChangePasswordSerializer

User = get_user_model()


# -------------------------
# Регистрация
# -------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer

# -------------------------
# Логин (JWT)
# -------------------------
class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

# -------------------------
# Обновление токена
# -------------------------
class TokenRefreshViewCustom(TokenRefreshView):
    pass


# -------------------------
# Logout (Blacklisting Refresh Token)
# -------------------------
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Успешный выход."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# Смена пароля
# -------------------------
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user


# -------------------------
# Отправка email (пример SMTP)
# -------------------------
class SendEmailView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        subject = request.data.get("subject", "Test email")
        message = request.data.get("message", "Hello from Django!")
        from_email = settings.EMAIL_HOST_USER

        # Простой красивый HTML-шаблон для письма
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: auto; background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #333;">{subject}</h2>
                    <p style="font-size: 16px; color: #555;">{message}</p>
                    <hr style="margin: 20px 0;">
                    <p style="font-size: 12px; color: #999;">Это автоматическое сообщение, не отвечайте на него.</p>
                </div>
            </body>
        </html>
        """

        try:
            send_mail(
                subject,
                message,
                from_email,
                [email],
                html_message=html_message
            )
            return Response({"detail": "Email успешно отправлен"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

