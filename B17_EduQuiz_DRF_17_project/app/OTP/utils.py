import secrets
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP

def generate_otp():
    return ''.join(secrets.choice(string.digits) for _ in range(6))

def send_otp_email(user_email):
    otp_code = generate_otp()
    OTP.objects.update_or_create(
        email=user_email,
        defaults={'code': otp_code}
    )

    subject = 'Ваш OTP код для подтверждения email'
    message = f"Ваш OTP код для подтверждения email: {otp_code}"
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
    except Exception as e:
        raise Exception(f"Ошибка при отправке email: {str(e)}")