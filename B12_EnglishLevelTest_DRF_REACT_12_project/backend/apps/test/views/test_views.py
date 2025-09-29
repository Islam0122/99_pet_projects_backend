from ..serializers import *
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from ..models import Test
from ..serializers import TestSerializer

class TestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Test.objects.all().prefetch_related('questions')
    serializer_class = TestSerializer
    permission_classes = [AllowAny]

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
