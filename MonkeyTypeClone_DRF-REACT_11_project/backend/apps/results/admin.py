from django.contrib import admin
from .models import TestResult


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "wpm",
        "accuracy",
        "timer_display",
        "category",
        "created_at",
    )
    list_filter = ("created_at", "category", "timer")
    search_fields = ("user__username", "user__email")
    ordering = ("-created_at",)

    def timer_display(self, obj):
        return f"{obj.timer.seconds} сек." if obj.timer else "—"
    timer_display.short_description = "Таймер"
