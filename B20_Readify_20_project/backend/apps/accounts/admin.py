from django.contrib import admin
from .models import TGUser


@admin.register(TGUser)
class TGUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "telegram_id",
        "xp",
        "total_read_books",
        "streak_days",
        "last_active",
    )
    list_display_links = ("id", "username")
    search_fields = ("username", "telegram_id")
    list_filter = ("streak_days", "created_at")
    readonly_fields = ("created_at", "last_active", "last_read_date")
    ordering = ("-streak_days", "-xp", "-created_at")

    fieldsets = (
        ("👤 Основная информация", {
            "fields": ("telegram_id", "username"),
        }),
        ("🔥 Активность пользователя", {
            "fields": ("xp", "total_read_books", "streak_days", "last_read_date", "last_active"),
        }),
        ("🕓 Системная информация", {
            "fields": ("created_at",),
        }),
    )

    def has_add_permission(self, request):
        """Запрещаем добавление пользователей вручную"""
        return False
