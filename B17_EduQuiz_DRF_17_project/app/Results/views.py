from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import ResultsTest
from .serializers import ResultsTestSerializer


class ResultsTestViewSet(viewsets.ModelViewSet):
    queryset = ResultsTest.objects.all().order_by('-created_at')
    serializer_class = ResultsTestSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()
