from rest_framework import serializers
from .models import Group, Student


class StudentSerializer(serializers.ModelSerializer):
    """Сериализатор для студентов"""

    group_title = serializers.CharField(
        source="group.title",
        read_only=True,
        help_text="Название группы, в которой учится студент"
    )

    progress_percent = serializers.SerializerMethodField(
        help_text="Процент выполнения домашних заданий студентом"
    )

    class Meta:
        model = Student
        fields = [
            "id",
            "full_name",
            "username",
            "telegram_id",
            "group",
            "group_title",
            "total_homeworks",
            "completed_homeworks",
            "progress_percent",
            "average_score",
            "best_score",
            "total_points",
            "rank",
            "progress_level",
            "is_active",
            "last_homework_done",
        ]
        read_only_fields = (
            "average_score",
            "best_score",
            "total_points",
            "rank",
            "progress_percent",
        )

    def get_progress_percent(self, obj):
        """Вычисляет процент выполненных заданий"""
        if obj.total_homeworks == 0:
            return 0
        return round((obj.completed_homeworks / obj.total_homeworks) * 100, 1)



class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для учебных групп"""

    students_count = serializers.SerializerMethodField(
        help_text="Количество студентов в группе"
    )
    students = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = [
            "id",
            "title",
            "description",
            "telegram_id",
            "students_count",
            "students",
        ]

    def get_students_count(self, obj):
        return obj.students.count()
