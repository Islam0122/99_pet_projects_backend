from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title"]
    search_fields = ["title"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "identification_number",
        "title",
        "category",
        "price",
        "sale_price",
        "is_archived",
        "created_at",
        "updated_at",
        "display_image",
    ]
    list_filter = ["category", "is_archived", "created_at", "updated_at"]
    search_fields = ["identification_number", "title", "description"]

    readonly_fields = ["display_image", "created_at", "updated_at"]

    fieldsets = (
        ("Основная информация", {
            "fields": ("identification_number", "title", "description", "category")
        }),
        ("Цены", {
            "fields": ("price", "sale_price")
        }),
        ("Медиа", {
            "fields": ("display_image", "image")
        }),
        ("Статус", {
            "fields": ("is_archived",)
        }),
        ("Системные данные", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" style="border-radius:5px;" />',
                obj.image.url
            )
        return "—"

    display_image.short_description = "Превью"
