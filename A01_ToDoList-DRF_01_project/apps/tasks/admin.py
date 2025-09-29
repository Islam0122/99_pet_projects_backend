from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at")
    fieldsets = (
        (None, {
            "fields": ("title", "description", "status")
        }),
        ("Дополнительно", {
            "fields": ("id", "created_at"),
            "classes": ("collapse",)  # скрытая секция
        }),
    )
