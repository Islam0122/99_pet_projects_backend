from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string


def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verification_link = (
        f"{request.scheme}://{request.get_host()}"
        f"/api/auth/verify-email/?token={token}&uid={uid}"
    )

    subject = 'Подтверждение email - Porter Kg'
    message = f'''
Здравствуйте, {user.first_name}!

Спасибо за регистрацию в Porter Kg!

Пожалуйста, подтвердите ваш email, перейдя по ссылке:
{verification_link}

Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.

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


def send_password_reset_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    reset_link = (
        f"{request.scheme}://{request.get_host()}"
        f"/api/auth/password-reset-confirm/?token={token}&uid={uid}"
    )

    subject = 'Сброс пароля - Porter Kg'
    message = f'''
Здравствуйте, {user.first_name}!

Вы запросили сброс пароля для вашего аккаунта в Porter Kg.

Перейдите по ссылке для создания нового пароля:
{reset_link}

Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.
Ваш пароль останется без изменений.

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


def send_welcome_email(user):
    subject = 'Добро пожаловать в Porter Kg!'
    message = f'''
Здравствуйте, {user.first_name}!

Добро пожаловать в Porter Kg - ваш надежный сервис для поездок и грузоперевозок!

Мы рады видеть вас в нашем сервисе. Теперь вы можете:
- Бронировать поездки
- Находить водителей
- Управлять своим профилем

Если у вас возникнут вопросы, наша служба поддержки всегда готова помочь.

С уважением,
Команда Porter Kg
    '''

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=True,
    )


def send_driver_verification_email(driver_profile):
    user = driver_profile.user

    subject = 'Верификация водителя - Porter Kg'
    message = f'''
Здравствуйте, {user.first_name}!

Поздравляем! Ваш аккаунт водителя успешно верифицирован.

Теперь вы можете:
- Принимать заказы
- Получать больше запросов от клиентов
- Участвовать в программе лояльности для верифицированных водителей

Желаем успешной работы!

С уважением,
Команда Porter Kg
    '''

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=True,
    )