"""
Views для аутентификации
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from drf_spectacular.utils import extend_schema, OpenApiParameter
from ..serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    GoogleAuthSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    EmailVerificationSerializer,
    TokenSerializer,
    UserSerializer
)
from ..models import GuestProfile
from ..utils.email import send_verification_email

User = get_user_model()


def get_tokens_for_user(user):
    """Генерация JWT токенов для пользователя"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={201: TokenSerializer},
        description="Регистрация нового пользователя"
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            try:
                send_verification_email(user, request)
            except Exception as e:
                print(f"Ошибка отправки email: {e}")

            tokens = get_tokens_for_user(user)

            return Response({
                'message': 'Регистрация успешна. Проверьте email для подтверждения.',
                'user': UserSerializer(user).data,
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @extend_schema(
        request=UserLoginSerializer,
        responses={200: TokenSerializer},
        description="Вход пользователя в систему"
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                if not user.is_active:
                    return Response({
                        'error': 'Аккаунт деактивирован'
                    }, status=status.HTTP_403_FORBIDDEN)

                tokens = get_tokens_for_user(user)

                return Response({
                    'message': 'Вход выполнен успешно',
                    'user': UserSerializer(user).data,
                    'tokens': tokens
                }, status=status.HTTP_200_OK)

            return Response({
                'error': 'Неверный email или пароль'
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Выход пользователя из системы"
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response({
                'message': 'Выход выполнен успешно'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Ошибка при выходе'
            }, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = GoogleAuthSerializer

    @extend_schema(
        request=GoogleAuthSerializer,
        responses={200: TokenSerializer},
        description="Аутентификация через Google OAuth2"
    )
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            try:
                CLIENT_ID = getattr(settings, 'GOOGLE_OAUTH2_CLIENT_ID', None)
                if not CLIENT_ID:
                    return Response({
                        'error': 'Google OAuth2 не настроен'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                idinfo = id_token.verify_oauth2_token(
                    token,
                    requests.Request(),
                    CLIENT_ID
                )

                email = idinfo['email']
                first_name = idinfo.get('given_name', '')
                last_name = idinfo.get('family_name', '')

                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'auth_type': 'google',
                        'is_verified': True,
                        'role': 'guest'
                    }
                )

                if created:
                    GuestProfile.objects.create(user=user)

                tokens = get_tokens_for_user(user)

                return Response({
                    'message': 'Вход через Google выполнен успешно',
                    'user': UserSerializer(user).data,
                    'tokens': tokens,
                    'created': created
                }, status=status.HTTP_200_OK)

            except ValueError:
                return Response({
                    'error': 'Неверный Google токен'
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({
                    'error': f'Ошибка аутентификации: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter('token', str, description='Токен подтверждения'),
            OpenApiParameter('uid', str, description='ID пользователя (base64)'),
        ],
        description="Подтверждение email адреса"
    )
    def get(self, request):
        token = request.GET.get('token')
        uid = request.GET.get('uid')

        if not token or not uid:
            return Response({
                'error': 'Отсутствуют необходимые параметры'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)

            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save(update_fields=['is_verified'])

                return Response({
                    'message': 'Email успешно подтвержден'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Неверный или устаревший токен'
                }, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'error': 'Неверная ссылка подтверждения'
            }, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=PasswordResetRequestSerializer,
        description="Запрос на сброс пароля"
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            try:
                user = User.objects.get(email=email)

                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                reset_link = f"{request.scheme}://{request.get_host()}/api/auth/password-reset-confirm/?token={token}&uid={uid}"

                subject = 'Сброс пароля - Porter Kg'
                message = f'''
Здравствуйте, {user.first_name}!

Вы запросили сброс пароля. Перейдите по ссылке для создания нового пароля:
{reset_link}

Если вы не запрашивали сброс пароля, проигнорируйте это письмо.

С уважением,
Команда Porter Kg
                '''

                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

            except User.DoesNotExist:
                pass  # Для безопасности не говорим, что пользователь не найден
            except Exception as e:
                return Response({
                    'error': 'Ошибка отправки email'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                'message': 'Инструкции по сбросу пароля отправлены на email'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        description="Подтверждение сброса пароля и установка нового"
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            uid = serializer.validated_data['uid']

            try:
                user_id = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=user_id)

                if default_token_generator.check_token(user, token):
                    user.set_password(serializer.validated_data['password'])
                    user.save()

                    return Response({
                        'message': 'Пароль успешно изменен'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Неверный или устаревший токен'
                    }, status=status.HTTP_400_BAD_REQUEST)

            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({
                    'error': 'Неверная ссылка сброса пароля'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserSerializer},
        description="Получение информации о текущем авторизованном пользователе"
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)