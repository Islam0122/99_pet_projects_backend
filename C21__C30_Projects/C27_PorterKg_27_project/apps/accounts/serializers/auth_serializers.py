"""
Сериализаторы для аутентификации
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from ..models import GuestProfile, DriverProfile
from .user_serializers import UserSerializer

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    role = serializers.ChoiceField(
        choices=['guest', 'driver'],
        required=True
    )

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'password',
            'password_confirm',
            'role'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Пароли не совпадают"
            })
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(
                "Пользователь с таким email уже существует"
            )
        return value.lower()

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        role = validated_data.pop('role')

        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            role=role,
            auth_type='local'
        )

        if role == 'guest':
            GuestProfile.objects.create(user=user)
        elif role == 'driver':
            DriverProfile.objects.create(
                user=user,
                phone_number='',
                driver_license_number='',
                driver_license_category=''
            )

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField(
        required=True,
        help_text="ID token от Google"
    )


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value.lower()).exists():
            pass
        return value.lower()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    uid = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Пароли не совпадают"
            })
        return attrs


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    uid = serializers.CharField(required=True)


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField(help_text="Access token")
    refresh = serializers.CharField(help_text="Refresh token")
    user = UserSerializer(help_text="Данные пользователя")