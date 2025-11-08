from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import TGUser


class TGUserSerializer(serializers.ModelSerializer):
    streak_status = serializers.SerializerMethodField()
    member_since = serializers.SerializerMethodField()

    class Meta:
        model = TGUser
        fields = [
            "id",
            "telegram_id",
            "username",
            "created_at",
            "total_task_completes",
            "streak_days",
            "last_task_completed",
            "streak_status",
            "member_since",
        ]
        read_only_fields = ("created_at", "last_task_completed")

    @extend_schema_field(serializers.CharField)
    def get_streak_status(self, obj):
        if obj.streak_days == 0:
            return "Не начинал streak 🌱"
        elif obj.streak_days < 3:
            return f"Начал streak — {obj.streak_days} дня подряд ⚡"
        elif obj.streak_days < 7:
            return f"Продолжает streak — {obj.streak_days} дней 🔥"
        else:
            return f"Легенда streak — {obj.streak_days} дней подряд 👑"

    @extend_schema_field(serializers.CharField)
    def get_member_since(self, obj):
        return obj.created_at.strftime("%d.%m.%Y, %H:%M") if obj.created_at else None
