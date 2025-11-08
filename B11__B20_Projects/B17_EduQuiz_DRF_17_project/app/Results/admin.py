from django.contrib import admin
from app.Results.models import ResultsTest
from django.utils.html import format_html

@admin.register(ResultsTest)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'topic', 'score', 'percentage', 'created_at', 'certificate_link')
    list_filter = ('topic', 'created_at')
    search_fields = ('name', 'email')
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'certificate_link')

    def certificate_link(self, obj):
        if obj.certificate:
            return format_html(
                '<a href="{}" target="_blank" style="padding: 5px 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">📜 Открыть сертификат</a>',
                obj.certificate.url
            )
        return format_html('<span style="color: #888;">Нет сертификата</span>')

    certificate_link.short_description = 'Сертификат'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
