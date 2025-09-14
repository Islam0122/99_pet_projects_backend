from rest_framework import serializers
from ..models import ResultsTest , PlacementTestResult


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


class PlacementTestResultCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания результата теста (до генерации сертификата)
    """
    class Meta:
        model = PlacementTestResult
        fields = [
            "id",
            "test",
            "name",
            "email",
            "total_questions",
            "level_a1_correct",
            "level_a2_correct",
            "level_b1_correct",
            "level_b2_correct",
            "level_c1_correct",
            "level_c2_correct",
        ]


class PlacementTestResultSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения результата вместе с сертификатом
    """
    test_name = serializers.CharField(source="test.name", read_only=True)
    level_title = serializers.CharField(source="level.title", read_only=True)
    certificate_url = serializers.SerializerMethodField()

    class Meta:
        model = PlacementTestResult
        fields = [
            "id",
            "test_name",
            "name",
            "email",
            "score",
            "level_title",
            "total_questions",
            "correct_answers",
            "wrong_answers",
            "percentage",
            "certificate_url",
            "created_at",
            "level_a1_correct",
            "level_a2_correct",
            "level_b1_correct",
            "level_b2_correct",
            "level_c1_correct",
            "level_c2_correct",
        ]

    def get_certificate_url(self, obj):
        """Возвращает абсолютный URL к PDF сертификату"""
        if obj.certificate:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.certificate.url) if request else obj.certificate.url
        return None

