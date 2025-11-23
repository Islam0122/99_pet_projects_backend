from rest_framework import generics, status, views, serializers
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import generics, permissions
from .models import UserModel
from .serializers import (
    UserRegistrationSerializer,
    OTPVerificationSerializer,
    UserFullProfileSerializer, UserSerializer, OTPAuthenticationSerializer
)

User = get_user_model()

# Регистрация пользователя
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]



# Профиль пользователя
class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Представление для работы с профилем пользователя:
    - Просмотр данных профиля.
    - Обновление данных профиля.
    """
    serializer_class = UserFullProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Возвращает текущего аутентифицированного пользователя
        return self.request.user



# 🔑 3. Список пользователей (только для администраторов)
class UserListView(generics.ListAPIView):
    """
    Получение списка пользователей (только для администраторов).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer




class ResendOTPView(generics.GenericAPIView):
    serializer_class = OTPVerificationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get("phone_number")

        if not phone_number:
            raise ValidationError({"phone_number": "Номер телефона обязателен."})

        serializer = self.get_serializer(data=request.data)
        try:
            response = serializer.resend_otp(phone_number)
            return Response(response)
        except serializers.ValidationError as e:
            return Response({"error": str(e)}, status=400)


class OTPAuthenticationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OTPAuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)