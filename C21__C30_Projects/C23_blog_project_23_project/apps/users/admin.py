from django.contrib import admin
from .models import UserToken, UserProfile


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token_preview', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'token')
    readonly_fields = ('token', 'created_at')
    date_hierarchy = 'created_at'

    def token_preview(self, obj):
        return f"{obj.token[:20]}..."

    token_preview.short_description = 'Token'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('bio', 'avatar')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )