from django.contrib import admin
from .models import BroadcastPrompt

@admin.register(BroadcastPrompt)
class BroadcastPromptAdmin(admin.ModelAdmin):
    list_display = ("title", "is_sent", "created_at", "sent_at")
    readonly_fields = ("is_sent", "sent_at", "created_at")
    search_fields = ("title", "prompt_text")

    def has_change_permission(self, request, obj = ...):
        return False