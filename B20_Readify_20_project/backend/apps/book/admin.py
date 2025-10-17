from django.contrib import admin
from .models import Book, Chapter


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

