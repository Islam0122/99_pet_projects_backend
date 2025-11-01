from django.contrib import admin
from .models import Group, Student
from django.contrib import admin
from django.utils.html import format_html
from ..homework.models import  Month1Homework, Month1HomeworkItem, Month2Homework, Month3Homework


# ===== Month 1 =====
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


class Month1HomeworkInline(admin.TabularInline):
    model = Month1Homework
    extra = 0
    fields = ("lesson", "created_at")
    readonly_fields = ("lesson", "created_at")
    inlines = [Month1HomeworkItemInline]


# ===== Month 2 =====
class Month2HomeworkInline(admin.TabularInline):
    model = Month2Homework
    extra = 0
    fields = ("title", "lesson", "grade", "is_checked_colored", "github_url", "created_at")
    readonly_fields = ("grade", "is_checked_colored", "created_at")

    def is_checked_colored(self, obj):
        color = "green" if obj.is_checked else "red"
        text = "Проверено" if obj.is_checked else "Не проверено"
        return format_html('<b><span style="color: {};">{}</span></b>', color, text)

    is_checked_colored.short_description = "Статус проверки"


# ===== Month 3 =====
class Month3HomeworkInline(admin.TabularInline):
    model = Month3Homework
    extra = 0
    fields = ("title", "lesson", "grade", "is_checked_colored", "github_url", "created_at")
    readonly_fields = ("grade", "is_checked_colored", "created_at")

    def is_checked_colored(self, obj):
        color = "green" if obj.is_checked else "red"
        text = "Проверено" if obj.is_checked else "Не проверено"
        return format_html('<b><span style="color: {};">{}</span></b>', color, text)

    is_checked_colored.short_description = "Статус проверки"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "telegram_id", "student_count", "description_short")
    search_fields = ("title", "telegram_id")
    ordering = ("title",)
    list_per_page = 20

    def student_count(self, obj):
        return obj.students.count()
    student_count.short_description = "Количество студентов"

    def description_short(self, obj):
        return (obj.description[:50] + "...") if obj.description else "-"
    description_short.short_description = "Описание"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "username",
        "group",
        "average_score",
        "best_score",
        "total_points",
        "completed_homeworks",
        "rank",
        "progress_level",
        "is_active",
    )
    list_filter = ("group", "progress_level", "is_active")
    search_fields = ("full_name", "username", "telegram_id")
    ordering = ("group", "-average_score")
    list_per_page = 25

    fieldsets = (
        ("👤 Основная информация", {
            "fields": ("full_name", "username", "telegram_id", "group", "is_active"),
            "description": "Основные данные о студенте и его принадлежность к группе."
        }),
        ("📊 Статистика", {
            "fields": (
                "total_homeworks",
                "completed_homeworks",
                "last_homework_done",
                "average_score",
                "best_score",
                "total_points",
                "rank",
                "progress_level",
            ),
            "description": "Учебная статистика и прогресс студента."
        }),

    )
    inlines = [Month1HomeworkInline, Month2HomeworkInline, Month3HomeworkInline]


    readonly_fields = (
        "average_score",
        "best_score",
        "rank",
        "last_homework_done",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("group")





