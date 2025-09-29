from django.contrib import admin
from .models import UserRecipe


@admin.register(UserRecipe)
class UserRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "category",
        "short_user_text",
        "short_ai_result",
        "created_at",
    )
    list_filter = ("category", "created_at")
    search_fields = ("user__username", "user_text", "ai_result")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def short_user_text(self, obj):
        return (obj.user_text[:50] + "...") if len(obj.user_text) > 50 else obj.user_text
    short_user_text.short_description = "Запрос пользователя"

    def short_ai_result(self, obj):
        if obj.ai_result:
            return (obj.ai_result[:70] + "...") if len(obj.ai_result) > 70 else obj.ai_result
        return "—"
    short_ai_result.short_description = "Рецепт AI"
