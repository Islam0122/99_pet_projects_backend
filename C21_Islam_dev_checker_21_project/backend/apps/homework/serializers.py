from rest_framework import serializers
from .models import Month1Homework, Month1HomeworkItem, Month2Homework, Month3Homework
from ..student.serializers import StudentSerializer  # если у тебя есть сериализатор студента


# ==== Month 1 ====
class Month1HomeworkItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month1HomeworkItem
        fields = [
            "id",
            "task_condition",
            "student_answer",
            "grade",
            "ai_feedback",
            "originality_check",
            "is_checked",
        ]


class Month1HomeworkSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    items = Month1HomeworkItemSerializer(many=True, read_only=True)

    class Meta:
        model = Month1Homework
        fields = [
            "id",
            "student",
            "lesson",
            "created_at",
            "items",
        ]


# ==== Month 2 ====
class Month2HomeworkSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Month2Homework
        fields = [
            "id",
            "student",
            "lesson",
            "title",
            "task_condition",
            "grade",
            "originality_check",
            "is_checked",
            "github_url",
            "file_presentation",
            "created_at",
        ]


# ==== Month 3 ====
class Month3HomeworkSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Month3Homework
        fields = [
            "id",
            "student",
            "lesson",
            "title",
            "task_condition",
            "grade",
            "originality_check",
            "is_checked",
            "github_url",
            "file_presentation",
            "created_at",
        ]
