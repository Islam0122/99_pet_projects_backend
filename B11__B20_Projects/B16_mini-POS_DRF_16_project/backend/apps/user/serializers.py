from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if user is None:
            raise serializers.ValidationError("Неверные учетные данные")

        if not user.is_allowed:
            raise serializers.ValidationError("Вам запрещен доступ")

        data["user"] = user
        return data


class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
