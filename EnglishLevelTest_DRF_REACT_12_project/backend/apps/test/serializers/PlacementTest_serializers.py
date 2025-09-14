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

    class Meta:
        model = PlacementTest
        fields = ["id", "name", "description", "questions"]

    def get_questions(self, obj):
        qs = obj.questions.all()
        levels = qs.values_list('level_id', flat=True).distinct().order_by('level_id')
        selected = []

        questions_per_level = 5

        for lvl in levels:
            lvl_qs = list(qs.filter(level_id=lvl))
            if len(lvl_qs) <= questions_per_level:
                selected.extend(lvl_qs)
            else:
                selected.extend(random.sample(lvl_qs, questions_per_level))
        random.shuffle(selected)
        return PlacementTestQuestionSerializer(selected, many=True).data

