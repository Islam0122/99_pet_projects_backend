from rest_framework import serializers
from .models import HomeWork, HwItem

class HwItemSerializer(serializers.ModelSerializer):
    short_task = serializers.SerializerMethodField()
    short_answer = serializers.SerializerMethodField()

    class Meta:
        model = HwItem
        fields = ["id", "task_condition", "short_task", "student_answer", "short_answer", "grade", "ai_feedback", "originality_check"]
        read_only_fields = ["grade", "ai_feedback", "originality_check"]

    def get_short_task(self, obj):
        return obj.task_condition[:60] + "..." if len(obj.task_condition) > 60 else obj.task_condition

    def get_short_answer(self, obj):
        return obj.student_answer[:60] + "..." if len(obj.student_answer) > 60 else obj.student_answer


class HomeWorkSerializer(serializers.ModelSerializer):
    items = HwItemSerializer(many=True, read_only=True)
    average_grade = serializers.SerializerMethodField()
    ai_status = serializers.SerializerMethodField()

    class Meta:
        model = HomeWork
        fields = ["id", "student_name", "student_email", "lesson", "created_at", "average_grade", "ai_status", "items"]
        read_only_fields = ["created_at"]

    def get_average_grade(self, obj):
        grades = [i.grade for i in obj.items.all() if i.grade is not None]
        if not grades:
            return None
        return round(sum(grades)/len(grades), 2)

    def get_ai_status(self, obj):
        if all(item.originality_check for item in obj.items.all()):
            if any("AI" in item.originality_check.upper() for item in obj.items.all()):
                return "Есть AI-текст"
            return "Оригинально"
        return "Не проверено"
