from django.contrib import admin
from .models import BusinessElement, AccessRolesRules


@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at', 'rules_count']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at']

    def rules_count(self, obj):
        return obj.access_rules.count()

    rules_count.short_description = 'Количество правил'


@admin.register(AccessRolesRules)
class AccessRolesRulesAdmin(admin.ModelAdmin):
    list_display = [
        'role',
        'element',
        'read_permission',
        'read_all_permission',
        'create_permission',
        'update_permission',
        'update_all_permission',
        'delete_permission',
        'delete_all_permission',
        'permissions_summary',
    ]
    list_filter = ['role', 'element', 'created_at']
    search_fields = ['role__name', 'element__name']
    ordering = ['role__name', 'element__name']

    fieldsets = (
        ('Основная информация', {
            'fields': ('role', 'element')
        }),
        ('Права на чтение', {
            'fields': ('read_permission', 'read_all_permission')
        }),
        ('Права на создание', {
            'fields': ('create_permission',)
        }),
        ('Права на обновление', {
            'fields': ('update_permission', 'update_all_permission')
        }),
        ('Права на удаление', {
            'fields': ('delete_permission', 'delete_all_permission')
        }),
        ('Информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    def permissions_summary(self, obj):
        return obj.get_permissions_summary()

    permissions_summary.short_description = 'Краткое описание прав'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('role', 'element')