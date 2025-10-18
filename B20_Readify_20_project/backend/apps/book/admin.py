from django.contrib import admin
from .models import Book, Chapter, UserBook


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1
    fields = ("number", "title", "text")
    ordering = ("number",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "total_chapters")
    search_fields = ("title", "author")
    list_filter = ("author",)
    inlines = [ChapterInline]



@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    list_display = ("title", "telegram_user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "description", "telegram_user__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Информация о книге", {
            "fields": ("title", "description", "file")
        }),
        ("Информация о пользователе", {
            "fields": ("telegram_user",)
        }),
        ("Системная информация", {
            "fields": ("created_at",),
        }),
    )