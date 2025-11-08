from django.contrib import admin
from .models import TGUser


@admin.register(TGUser)
class TGUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "telegram_id",
        "streak_days",
        "total_task_completes",
        "last_task_completed",
        "created_at",
    )
    list_display_links = ("id", "username")
    search_fields = ("username", "telegram_id")
    list_filter = ("created_at", "streak_days")
    readonly_fields = ("created_at", "last_task_completed")
    ordering = ("-streak_days", "-created_at")

    fieldsets = (
        ("👤 Основная информация", {
            "fields": ("telegram_id", "username"),
            "description": "Основные данные пользователя Telegram",
        }),
        ("🔥 Активность пользователя", {
            "fields": ("streak_days", "total_task_completes", "last_task_completed"),
            "description": "Информация о выполнении задач и серии подряд",
        }),
        ("🕓 Системная информация", {
            "fields": ("created_at",),
        }),
    )

    def has_add_permission(self, request):
        return False
