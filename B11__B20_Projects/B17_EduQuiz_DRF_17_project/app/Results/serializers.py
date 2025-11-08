from rest_framework import serializers
from .models import ResultsTest

class ResultsTestSerializer(serializers.ModelSerializer):
    certificate_url = serializers.SerializerMethodField()

    class Meta:
        model = ResultsTest
        fields = [
            'id',
            'topic',
            'name',
            'email',
            'score',
            'total_questions',
            'correct_answers',
            'wrong_answers',
            'percentage',
            'certificate_url',
            'created_at',
        ]

    def get_certificate_url(self, obj):
        request = self.context.get('request')
        if obj.certificate and request:
            return request.build_absolute_uri(obj.certificate.url)
        return None
