from rest_framework import serializers
from ..models import ResultsTest


class ResultsTestCreateSerializer(serializers.ModelSerializer):
    """Используется для создания результата теста (до генерации сертификата)"""
    class Meta:
        model = ResultsTest
        fields = [
            "id",
            "test",
            "name",
            "email",
            "score",
            "total_questions",
            "correct_answers",
            "wrong_answers",
            "percentage",
        ]


class ResultsTestSerializer(serializers.ModelSerializer):
    """Используется для вывода результата вместе с сертификатом"""
    test_name = serializers.CharField(source="test.name", read_only=True)
    level = serializers.CharField(source="test.level.title", read_only=True)

    class Meta:
        model = ResultsTest
        fields = [
            "id",
            "test",
            "test_name",
            "level",
            "name",
            "email",
            "score",
            "total_questions",
            "correct_answers",
            "wrong_answers",
            "percentage",
            "certificate",
            "created_at",
        ]
