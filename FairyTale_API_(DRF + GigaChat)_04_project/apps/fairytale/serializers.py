from rest_framework import serializers
from .models import FairyTale

class FairyTaleRequestSerializer(serializers.Serializer):
    """
    Сериализатор для запроса генерации сказки через GigaChat
    """
    title = serializers.CharField(max_length=255)
    characters = serializers.ListField(
        child=serializers.CharField(),
        help_text="Список персонажей сказки"
    )
    style = serializers.CharField(default="сказочный")
    length = serializers.ChoiceField(choices=["short", "medium", "long"], default="medium")


class FairyTaleSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения сказки
    """
    class Meta:
        model = FairyTale
        fields = ["id", "title", "story", "created_at"]


