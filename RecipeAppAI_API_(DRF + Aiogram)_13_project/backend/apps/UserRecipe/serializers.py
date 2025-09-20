from rest_framework import serializers
from .models import UserRecipe


class UserRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecipe
        fields = ["id", "user", "category", "user_text", "ai_result", "created_at"]
        read_only_fields = ["id", "created_at", "ai_result"]
