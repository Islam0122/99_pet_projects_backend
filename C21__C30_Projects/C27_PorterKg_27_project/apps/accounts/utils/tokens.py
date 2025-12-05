from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_verification_token(user):
    """
    Генерация токена для верификации email
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    return token, uid


def verify_token(token, uid):
    """
    Проверка токена верификации
    Возвращает пользователя если токен валидный, иначе None
    """
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)

        if default_token_generator.check_token(user, token):
            return user
        return None
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None


def is_token_valid(token, uid):
    """
    Проверка валидности токена без возврата пользователя
    """
    return verify_token(token, uid) is not None