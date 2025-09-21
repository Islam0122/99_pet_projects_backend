from django.contrib import admin
from .models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "full_name", "language", "telegram_id", "created_at", "joined_at")
    list_filter = ("created_at", "joined_at")
    search_fields = ("username", "full_name", "telegram_id")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "joined_at")
