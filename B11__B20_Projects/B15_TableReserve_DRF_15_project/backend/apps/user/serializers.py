from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
import requests


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'is_verified', 'password', 'password2', 'auth_type')
        read_only_fields = ('id', 'auth_type', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.auth_type = 'local'
        user.role = 'user'
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'auth_type', 'role', 'is_verified')
        read_only_fields = ('id', 'auth_type', 'role')


class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('token')
        if not token:
            raise serializers.ValidationError("Token не предоставлен")

        resp = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
        if resp.status_code != 200:
            raise serializers.ValidationError("Неверный Google токен")

        data = resp.json()
        email = data.get("email")
        if not email:
            raise serializers.ValidationError("Email не найден в токене")

        attrs['email'] = email
        return attrs
