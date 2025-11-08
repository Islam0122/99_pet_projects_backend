from django.contrib import admin
from .models import FairyTale
from django.utils.html import format_html

@admin.register(FairyTale)
class FairyTaleAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "story")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

