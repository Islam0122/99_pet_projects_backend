from django.contrib import admin
from .models import Group, Student


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

    readonly_fields = (
        "average_score",
        "best_score",
        "total_points",
        "rank",
        "last_homework_done",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("group")

    def has_add_permission(self, request):
        return False



