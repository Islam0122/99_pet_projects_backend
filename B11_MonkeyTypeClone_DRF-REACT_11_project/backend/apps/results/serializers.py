from rest_framework import serializers
from .models import TestResult
from ..user.models import User


class TestResultSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    timer_seconds = serializers.IntegerField(source="timer.seconds", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = TestResult
        fields = [
            "id",
            "user",           # FK на юзера (id)
            "user_username",  # красивое имя юзера
            "wpm",
            "accuracy",
            "timer",          # FK на таймер (id)
            "timer_seconds",  # время в секундах
            "category",       # FK на категорию (id)
            "category_name",  # название категории
            "created_at"
        ]
        read_only_fields = [
            "id", "user", "user_username",
            "created_at", "timer_seconds", "category_name"
        ]


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "best_wpm", "average_accuracy"]
