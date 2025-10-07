from django.contrib import admin
from .models import HomeWork, HwItem

class HwItemInline(admin.TabularInline):
    model = HwItem
    extra = 0
    readonly_fields = ("task_condition", "student_answer", "grade", "ai_feedback", "originality_check")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False  # запрещаем добавление вручную


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    list_display = ("student_name", "student_email", "lesson", "created_at", "average_grade", "ai_status")
    search_fields = ("student_name", "student_email", "lesson")
    list_filter = ("lesson", "created_at")
    readonly_fields = ("student_name", "student_email", "lesson", "created_at")
    inlines = [HwItemInline]

    def average_grade(self, obj):
        grades = [item.grade for item in obj.items.all() if item.grade is not None]
        if not grades:
            return "-"
        return round(sum(grades)/len(grades), 1)
    average_grade.short_description = "Средняя оценка"

    def ai_status(self, obj):
        if all(item.originality_check for item in obj.items.all()):
            if any("AI" in item.originality_check.upper() for item in obj.items.all()):
                return "Есть AI-текст"
            return "Оригинально"
        return "Не проверено"
    ai_status.short_description = "Статус AI-проверки"

    def has_add_permission(self, request):
        return False  # запрещаем создание вручную


@admin.register(HwItem)
class HwItemAdmin(admin.ModelAdmin):
    list_display = ("homework", "short_task", "colored_grade", "short_feedback")
    search_fields = ("homework__student_name", "task_condition", "student_answer")
    readonly_fields = ("homework", "task_condition", "student_answer", "grade", "ai_feedback", "originality_check")

    def short_task(self, obj):
        return (obj.task_condition[:50] + "...") if len(obj.task_condition) > 50 else obj.task_condition
    short_task.short_description = "Условие"

    def short_feedback(self, obj):
        if not obj.ai_feedback:
            return "-"
        return (obj.ai_feedback[:40] + "...") if len(obj.ai_feedback) > 40 else obj.ai_feedback
    short_feedback.short_description = "Комментарий"

    def colored_grade(self, obj):
        if obj.grade is None:
            return "-"
        color = "red" if obj.grade < 5 else "orange" if obj.grade < 8 else "green"
        return f"{obj.grade}/10"
    colored_grade.short_description = "Оценка"
