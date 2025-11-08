from django.contrib import admin
from .models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'location', 'is_active', 'created_at', 'updated_at')
    list_filter = ('location', 'is_active', 'created_at')
    search_fields = ('number',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('number',)
