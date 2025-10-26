from django.contrib import admin
from django.utils.html import format_html
from .models import Month1Homework, Month1HomeworkItem, Month2Homework, Month3Homework

# ==== Month 1 ====
class Month1HomeworkItemInline(admin.TabularInline):
    model = Month1HomeworkItem
    extra = 0
    fields = ("task_condition", "student_answer", "grade", "is_checked_colored", "ai_feedback", "originality_check")
    readonly_fields = ("ai_feedback", "originality_check", "is_checked_colored")
    show_change_link = True

    def is_checked_colored(self, obj):
        color = "green" if obj.is_checked else "red"
        text = "Проверено" if obj.is_checked else "Не проверено"
        return format_html('<b><span style="color: {};">{}</span></b>', color, text)
    is_checked_colored.short_description = "Статус проверки"

@admin.register(Month1Homework)
class Month1HomeworkAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "created_at")
    list_filter = ("lesson", "created_at")
    search_fields = ("student__full_name", "lesson")
    inlines = [Month1HomeworkItemInline]
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    fieldsets = (
        (None, {
            "fields": ("student", "lesson", "created_at")
        }),
    )


# ==== Month 2 ====
@admin.register(Month2Homework)
class Month2HomeworkAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "title", "colored_grade", "colored_checked", "created_at")
    list_filter = ("lesson", "is_checked", "created_at")
    search_fields = ("student__full_name", "lesson", "title")
    readonly_fields = ("created_at", "originality_check")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {
            "fields": ("student", "lesson", "title", "task_condition", "grade", "is_checked", "github_url", "file_presentation", "originality_check", "created_at")
        }),
    )

    def colored_checked(self, obj):
        color = "green" if obj.is_checked else "red"
        text = "Проверено" if obj.is_checked else "Не проверено"
        return format_html('<b><span style="color: {};">{}</span></b>', color, text)
    colored_checked.short_description = "Статус проверки"

    def colored_grade(self, obj):
        if obj.grade is None:
            return "-"
        if obj.grade >= 8:
            color = "green"
        elif obj.grade >= 5:
            color = "orange"
        else:
            color = "red"
        return format_html('<b><span style="color: {};">{}</span></b>', color, obj.grade)
    colored_grade.short_description = "Оценка"


# ==== Month 3 ====
@admin.register(Month3Homework)
class Month3HomeworkAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "title", "colored_grade", "colored_checked", "created_at")
    list_filter = ("lesson", "is_checked", "created_at")
    search_fields = ("student__full_name", "lesson", "title")
    readonly_fields = ("created_at", "originality_check")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {
            "fields": ("student", "lesson", "title", "task_condition", "grade", "is_checked", "github_url",  "originality_check", "created_at")
        }),
    )

    def colored_checked(self, obj):
        color = "green" if obj.is_checked else "red"
        text = "Проверено" if obj.is_checked else "Не проверено"
        return format_html('<b><span style="color: {};">{}</span></b>', color, text)
    colored_checked.short_description = "Статус проверки"

    def colored_grade(self, obj):
        if obj.grade is None:
            return "-"
        if obj.grade >= 8:
            color = "green"
        elif obj.grade >= 5:
            color = "orange"
        else:
            color = "red"
        return format_html('<b><span style="color: {};">{}</span></b>', color, obj.grade)
    colored_grade.short_description = "Оценка"
