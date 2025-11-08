from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Topic, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    readonly_fields = ("created_at", "updated_at", "preview_image")

    def preview_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image}" width="100" style="border-radius:5px;" />')
        return "Нет изображения"

    preview_image.short_description = "Превью изображения"


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "difficulty", "is_active", "created_at", "created_by", "num_questions")
    list_filter = ("difficulty", "is_active", "created_at")
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    list_editable = ("is_active",)
    readonly_fields = ("created_at", "updated_at","created_by","updated_user","num_questions")
    inlines = [QuestionInline]

    fieldsets = (
        ("Основная информация", {
            "fields": ("name", "description", "difficulty", "is_active")
        }),
        ("Дополнительная информация", {
            "fields": ("created_by","updated_user", "num_questions", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def num_questions(self, obj):
        return obj.questions.count()

    def save_model(self, request, obj, form, change):
        """Автоматически устанавливаем create_user и updated_user"""
        if not obj.pk:  # Если запись создаётся впервые
            obj.created_by = request.user
        obj.updated_user = request.user
        super().save_model(request, obj, form, change)
    num_questions.short_description = "Количество вопросов"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("short_text", "topic", "correct_answer", "is_active", "created_at", "created_by", "preview_image")
    list_filter = ("topic", "is_active", "created_at")
    search_fields = ("text", "topic__name")
    ordering = ("-created_at",)
    list_editable = ("is_active",)
    readonly_fields = ("created_at", "updated_at","created_by", "preview_image")

    fieldsets = (
        ("Основная информация", {
            "fields": ("topic", "text", "image", "preview_image", "is_active"),
        }),
        ("Варианты ответов", {
            "fields": ("option_a", "option_b", "option_c", "option_d", "correct_answer"),
            "classes": ("collapse",)  # Блок сворачивается
        }),
        ("Дополнительная информация", {
            "fields": ("created_by", "created_at", "updated_at"),
            "classes": ("collapse",)  # Блок сворачивается
        }),
    )
    def save_model(self, request, obj, form, change):
        """Автоматически устанавливаем create_user и updated_user"""
        if not obj.pk:  # Если запись создаётся впервые
            obj.created_by = request.user
        obj.updated_user = request.user
        super().save_model(request, obj, form, change)

    def short_text(self, obj):
        """Обрезанный текст вопроса для компактного отображения"""
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text

    short_text.short_description = "Вопрос"

    def preview_image(self, obj):
        """Отображает превью изображения, если оно есть"""
        if obj.image:
            return mark_safe(f'<img src="{obj.image}" width="100" style="border-radius:5px;" />')
        return "Нет изображения"

    preview_image.short_description = "Превью изображения"
