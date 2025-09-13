import random
from rest_framework import serializers
from ..models import PlacementTest, PlacementTest_Question
from .level_serializers import LevelSerializer


class PlacementTestQuestionSerializer(serializers.ModelSerializer):
    level = LevelSerializer(read_only=True)

    class Meta:
        model = PlacementTest_Question
        fields = [
            "id",
            "text",
            "question_type",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "correct_answer",
            "level",
            "image",
            "audio_file",
        ]


class PlacementTestSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    total_questions = serializers.SerializerMethodField()

    class Meta:
        model = PlacementTest
        fields = ["id", "name", "description", "questions", "total_questions"]

    def get_questions(self, obj):
        qs = list(obj.questions.all())
        if len(qs) <= 20:
            selected = qs
        else:
            selected = random.sample(qs, 30)  # выбираем случайные 30 вопросов
        return PlacementTestQuestionSerializer(selected, many=True).data

    def get_total_questions(self, obj):
        return obj.questions.count() - 20
