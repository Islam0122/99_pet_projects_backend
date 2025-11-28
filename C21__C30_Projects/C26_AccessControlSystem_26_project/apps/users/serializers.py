from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from .models import User
import random
import smtplib
from email.mime.text import MIMEText
import jwt


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email уже зарегистрирован"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        self.send_otp_email(user)
        return user

    def send_otp_email(self, user):
        otp = str(random.randint(100000, 999999))
        user.otp_code = otp
        user.otp_expires_at = timezone.now() + timedelta(minutes=10)
        user.save()

        subject = "Ваш OTP код для подтверждения email"
        body = f"Привет, {user.first_name}! Ваш код для подтверждения: {otp}. Он действует 10 минут."

        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = settings.EMAIL_HOST_USER
            msg['To'] = user.email

            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, [user.email], msg.as_string())
            server.quit()
        except Exception as e:
            print(f"Ошибка отправки OTP: {e}")


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        otp_code = attrs.get('otp_code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        if user.is_verified:
            raise serializers.ValidationError("Пользователь уже подтверждён")

        if user.otp_code != otp_code:
            raise serializers.ValidationError("Неверный OTP код")

        if timezone.now() > user.otp_expires_at:
            raise serializers.ValidationError("OTP код истёк")

        user.is_verified = True
        user.otp_code = None
        user.otp_expires_at = None
        user.save()

        attrs['user'] = user
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Неверные данные для входа")
        if not user.is_active:
            raise serializers.ValidationError("Пользователь деактивирован")
        if not user.is_verified:
            raise serializers.ValidationError("Email не подтверждён")

        payload = {"user_id": user.id, "email": user.email}
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        attrs['token'] = token
        return attrs


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError("Email уже используется")
        return value


class SoftDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = []

    def save(self, **kwargs):
        user = self.instance
        user.is_active = False
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_verified', 'date_joined']
        read_only_fields = fields
