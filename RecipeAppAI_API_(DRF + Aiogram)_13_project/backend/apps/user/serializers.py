from .models import TgUser
from rest_framework import serializers

class TgUserSerializer(serializers.ModelSerializer):
    username_with_at = serializers.SerializerMethodField()

    class Meta:
        model = TgUser
        fields = [
            "id",
            "username",
            "username_with_at",
            "full_name",
            "telegram_id",
            "created_at",
            "joined_at",
        ]
        read_only_fields = ["id", "created_at", "joined_at"]

    def get_username_with_at(self, obj):
        return f"@{obj.username}" if obj.username else None

