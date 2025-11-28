from django.core.exceptions import ValidationError
import re

def validate_password_strength(value):
    if len(value) < 6:
        raise ValidationError("Пароль должен быть минимум 6 символов.")
    if not re.search(r'\d', value):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру.")
    if not re.search(r'[A-Za-z]', value):
        raise ValidationError("Пароль должен содержать хотя бы одну букву.")

def validate_otp_code(value):
    if not value.isdigit() or len(value) != 6:
        raise ValidationError("OTP код должен быть 6-значным числом.")

def validate_email_unique(email, user_model, user_instance=None):
    qs = user_model.objects.filter(email=email)
    if user_instance:
        qs = qs.exclude(id=user_instance.id)
    if qs.exists():
        raise ValidationError("Email уже используется.")
