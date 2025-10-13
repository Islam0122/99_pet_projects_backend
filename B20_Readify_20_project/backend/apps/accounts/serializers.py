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
            "xp",
            "level",
            "rank",
            "total_read_books",
            "streak_days",
            "streak_status",
            "last_read_date",
            "last_active",
            "member_since",
        ]
        read_only_fields = (
            "created_at",
            "last_active",
            "level",
            "rank",
            "streak_days",
        )

    @extend_schema_field(serializers.CharField)
    def get_streak_status(self, obj):
        """Красивое описание streak’а"""
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
        """Форматирует дату регистрации"""
        return obj.created_at.strftime("%d.%m.%Y, %H:%M") if obj.created_at else None

    def update(self, instance, validated_data):
        """Автоматически обновляет XP, уровень, звание и last_active"""
        xp_before = instance.xp
        instance = super().update(instance, validated_data)
        if instance.xp != xp_before:
            instance.add_xp(instance.xp - xp_before)
        instance.update_activity()

        return instance
