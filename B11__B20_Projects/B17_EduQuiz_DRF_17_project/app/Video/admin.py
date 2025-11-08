from django.contrib import admin
from .models import Video, VideoCategory


class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', )
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
    )

admin.site.register(VideoCategory, VideoCategoryAdmin)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_url','video_category', 'created_at', 'is_active')
    search_fields = ('title', 'video_url', 'description')  # Теперь ищем по полю description
    list_filter = ('created_at', 'is_active')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description','video_category', 'video_url', 'is_active')  # Добавили description
        }),
        ('Дополнительная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at',)

admin.site.register(Video, VideoAdmin)
