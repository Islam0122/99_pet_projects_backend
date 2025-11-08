from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Task


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий."""
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {
            "fields": ("name",)
        }),
        ("Системная информация", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )

    verbose_name = "Категория"
    verbose_name_plural = "Категории"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Админка для задач."""
    list_display = (
        "colored_title",
        "owner",
        "get_categories",
        "due_date",
        "colored_status",
        "created_at",
    )
    list_filter = ("done", "categories", "due_date", "created_at")
    search_fields = ("title", "description", "owner__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at","due_reminder_sent","created_reminder_sent")
    filter_horizontal = ("categories",)

    fieldsets = (
        ("Основная информация", {
            "fields": ("title", "description", "owner", "categories")
        }),
        ("Статус и сроки", {
            "fields": ("done", "due_date")
        }),
        ("Системная информация", {
            "fields": ("created_at","due_reminder_sent","created_reminder_sent"),
            "classes": ("collapse",)
        }),
    )

    @admin.display(description="Название")
    def colored_title(self, obj):
        color = "#28a745" if obj.done else "#dc3545"
        return format_html('<b style="color: {};">{}</b>', color, obj.title)

    @admin.display(description="Категории")
    def get_categories(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])

    @admin.display(description="Статус")
    def colored_status(self, obj):
        if obj.done:
            return format_html('<span style="color: #28a745;">✅ Выполнена</span>')
        return format_html('<span style="color: #dc3545;">🕓 В процессе</span>')

    verbose_name = "Задача"
    verbose_name_plural = "Задачи"
