from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import PlacementTest, PlacementTest_Question
from ..serializers import PlacementTestSerializer, PlacementTestQuestionSerializer


class PlacementTestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet только для чтения PlacementTest
    list -> /placement-tests/
    retrieve -> /placement-tests/<id>/
    """
    queryset = PlacementTest.objects.all()
    serializer_class = PlacementTestSerializer

    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """
        Получить вопросы конкретного теста по id
        /placement-tests/<id>/questions/
        """
        test = self.get_object()
        questions = test.questions.all()
        serializer = PlacementTestQuestionSerializer(questions, many=True)
        # Можно убрать correct_answer для студента
        for q in serializer.data:
            q.pop('correct_answer', None)
        return Response(serializer.data)
