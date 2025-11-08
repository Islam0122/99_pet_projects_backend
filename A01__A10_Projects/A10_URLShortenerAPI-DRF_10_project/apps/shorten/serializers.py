from rest_framework import serializers
from .models import Link
from django.utils import timezone
from datetime import timedelta


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            "id",
            "original_url",
            "short_code",
            "clicks",
            "expires_at",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "clicks", "is_active", "created_at", "expires_at"]

    def create(self, validated_data):
        """
        При создании ссылки:
        - если short_code не передан, можно автоматически сгенерировать
        - expires_at автоматически ставится на 2 минуты
        - is_active = True
        """
        if "short_code" not in validated_data or not validated_data["short_code"]:
            import random, string
            validated_data["short_code"] = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        link = Link.objects.create(**validated_data)
        return link



