from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Group, Student, HomeWork, HwItem


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "group")
    search_fields = ("name", "email", "group__title")
    list_filter = ("group",)


class HwItemInline(admin.TabularInline):
    model = HwItem
    extra = 0
    readonly_fields = ("task_condition", "student_answer", "grade", "ai_feedback", "originality_check")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "created_at", "average_grade", "ai_status")
    list_filter = ("lesson", "created_at")
    search_fields = ("student__name", "student__email", "lesson")
    readonly_fields = ("student", "lesson", "created_at")
    inlines = [HwItemInline]

    def average_grade(self, obj):
        grades = [item.grade for item in obj.items.all() if item.grade is not None]
        return round(sum(grades)/len(grades), 1) if grades else "-"
    average_grade.short_description = "Средняя оценка"

    def ai_status(self, obj):
        if all(item.originality_check for item in obj.items.all()):
            if any("AI" in item.originality_check.upper() for item in obj.items.all()):
                color = "red"
                text = "Есть AI-текст"
            else:
                color = "green"
                text = "Оригинально"
        else:
            color = "gray"
            text = "Не проверено"
        return mark_safe(f'<b style="color:{color}">{text}</b>')
    ai_status.short_description = "Статус AI-проверки"


@admin.register(HwItem)
class HwItemAdmin(admin.ModelAdmin):
    list_display = ("homework", "short_task", "colored_grade", "short_feedback")
    search_fields = ("homework__student__name", "task_condition", "student_answer")
    readonly_fields = ("homework", "task_condition", "student_answer", "grade", "ai_feedback", "originality_check")

    def short_task(self, obj):
        return (obj.task_condition[:60] + "...") if len(obj.task_condition) > 60 else obj.task_condition
    short_task.short_description = "Условие"

    def short_feedback(self, obj):
        if not obj.ai_feedback:
            return "-"
        text = obj.ai_feedback.replace("\n", " ")[:60]
        return (text + "...") if len(text) > 60 else text
    short_feedback.short_description = "Комментарий"

    def colored_grade(self, obj):
        if obj.grade is None:
            return "-"
        color = "red" if obj.grade < 5 else "orange" if obj.grade < 8 else "green"
        return mark_safe(f'<b style="color:{color}">{obj.grade}/10</b>')
    colored_grade.short_description = "Оценка"
