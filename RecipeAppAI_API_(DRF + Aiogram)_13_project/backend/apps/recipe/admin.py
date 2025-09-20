from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "created_at", "updated_at")
    search_fields = ("title", "ingredients", "instructions")
    list_filter = ("category",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("title",)
