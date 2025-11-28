from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import logout
from .models import User
from .serializers import (
    RegisterSerializer,
    VerifyOtpSerializer,
    LoginSerializer,
    UpdateProfileSerializer,
    SoftDeleteSerializer,
    ProfileSerializer
)
from .permissions import IsAuthenticatedAndVerified


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "message": "Пользователь успешно зарегистрирован. Проверьте email для подтверждения.",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_verified": user.is_verified
            }
        }, status=status.HTTP_201_CREATED)


class VerifyOtpView(generics.GenericAPIView):
    serializer_class = VerifyOtpSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        return Response({
            "message": "Email успешно подтверждён",
            "user": {
                "id": user.id,
                "email": user.email,
                "is_verified": user.is_verified
            }
        }, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            "message": "Успешный вход",
            "token": serializer.validated_data['token']
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticatedAndVerified])
def logout_view(request):
    logout(request)
    return Response({
        "message": "Успешный выход из системы"
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticatedAndVerified])
def profile_view(request):
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        if 'email' in request.data and request.data['email'] != instance.email:
            user.is_verified = False
            user.save()
            return Response({
                "message": "Профиль обновлён. Требуется подтверждение нового email.",
                "user": ProfileSerializer(user).data
            }, status=status.HTTP_200_OK)

        return Response({
            "message": "Профиль успешно обновлён",
            "user": ProfileSerializer(user).data
        }, status=status.HTTP_200_OK)


class SoftDeleteView(generics.DestroyAPIView):
    serializer_class = SoftDeleteSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer.save()
        logout(request)

        return Response({
            "message": "Аккаунт успешно деактивирован"
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticatedAndVerified])
def test_protected_view(request):
    return Response({
        "message": f"Добро пожаловать, {request.user.first_name}!",
        "user": {
            "id": request.user.id,
            "email": request.user.email,
            "roles": [ur.role.name for ur in request.user.roles.all()]
        }
    }, status=status.HTTP_200_OK)