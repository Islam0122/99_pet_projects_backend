import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from apps.users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header:
            return None

        if not auth_header.startswith('Bearer '):
            return None

        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            raise exceptions.AuthenticationFailed('Неверный формат токена')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Токен истёк')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Неверный токен')

        user_id = payload.get('user_id')
        if not user_id:
            raise exceptions.AuthenticationFailed('Токен не содержит user_id')

        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Пользователь не найден')

        return (user, None)
    def authenticate_header(self, request):
        return 'Bearer realm="api"'