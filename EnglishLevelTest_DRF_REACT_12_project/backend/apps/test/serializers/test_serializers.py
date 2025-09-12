import random
from rest_framework import serializers
from ..models import Level, Test, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id", "text", "question_type",
            "option_a", "option_b", "option_c", "option_d",
            "correct_answer", "translation", "image", "audio_file"
        ]


class TestSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            "id", "name", "description", "level",
            "created_at", "updated_at",
            "questions", "total_questions",
        ]

    def get_questions(self, obj):
        qs = list(obj.questions.all())
        if len(qs) <= 20:
            return QuestionSerializer(qs, many=True).data
        selected = random.sample(qs, 20)
        return QuestionSerializer(selected, many=True).data

    def get_total_questions(self, obj):
        return obj.questions.count() - 30

