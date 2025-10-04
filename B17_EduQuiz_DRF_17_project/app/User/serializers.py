from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        print(user)

        if user is None:
            raise serializers.ValidationError("Неверные учетные данные")

        if not user.is_allowed:
            raise serializers.ValidationError("Вам запрещен доступ")

        data["user"] = user

        return data
