from rest_framework import serializers
from .models import HomeWork, HwItem, Student


class StudentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели студента."""

    class Meta:
        model = Student
        fields = ["id", "name", "email", "group"]


class HwItemSerializer(serializers.ModelSerializer):
    """Сериализатор для отдельного задания (пункта домашней работы)."""

    short_task = serializers.SerializerMethodField()
    short_answer = serializers.SerializerMethodField()

    class Meta:
        model = HwItem
        fields = [
            "id",
            "task_condition",
            "short_task",
            "student_answer",
            "short_answer",
            "grade",
            "ai_feedback",
            "originality_check",
        ]
        read_only_fields = ["grade", "ai_feedback", "originality_check"]

    def get_short_task(self, obj):
        """Возвращает сокращённый вариант условия задания."""
        text = obj.task_condition or ""
        return text[:60] + "..." if len(text) > 60 else text

    def get_short_answer(self, obj):
        """Возвращает сокращённый вариант ответа ученика."""
        text = obj.student_answer or ""
        return text[:60] + "..." if len(text) > 60 else text


class HomeWorkSerializer(serializers.ModelSerializer):
    """Сериализатор для домашнего задания."""

    items = HwItemSerializer(many=True, read_only=True)
    average_grade = serializers.SerializerMethodField()
    ai_status = serializers.SerializerMethodField()
    student_info = StudentSerializer(source="student", read_only=True)

    class Meta:
        model = HomeWork
        fields = [
            "id",
            "student",
            "student_info",
            "lesson",
            "created_at",
            "average_grade",
            "ai_status",
            "items",
        ]
        read_only_fields = ["created_at"]

    def get_average_grade(self, obj):
        """Возвращает средний балл по всем пунктам задания."""
        grades = [item.grade for item in obj.items.all() if item.grade is not None]
        return round(sum(grades) / len(grades), 2) if grades else None

    def get_ai_status(self, obj):
        """
        Проверяет оригинальность ответов:
        - если во всех пунктах есть анализ — выводит 'Оригинально' или 'Есть AI-текст'
        - если нет анализа — 'Не проверено'
        """
        items = obj.items.all()

        if not items.exists():
            return "Нет заданий"

        if all(item.originality_check for item in items):
            if any("AI" in (item.originality_check or "").upper() for item in items):
                return "Есть AI-текст"
            return "Оригинально"

        return "Не проверено"
