from django.contrib import admin
from .models import Category, Text, Timer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_per_page = 20

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "short_text")
    list_filter = ("category",)
    search_fields = ("text_content",)
    list_per_page = 20
    def short_text(self, obj):
        return obj.text_content[:50] + "..." if len(obj.text_content) > 50 else obj.text_content
    short_text.short_description = "Краткий текст"


@admin.register(Timer)
class TimerAdmin(admin.ModelAdmin):
    list_display = ("id", "formatted_time")
    search_fields = ("seconds",)
    list_per_page = 20

    def formatted_time(self, obj):
        """Форматирует секунды в ЧЧ:ММ:СС"""
        hours, remainder = divmod(obj.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    formatted_time.short_description = "Время (ЧЧ:ММ:СС)"
