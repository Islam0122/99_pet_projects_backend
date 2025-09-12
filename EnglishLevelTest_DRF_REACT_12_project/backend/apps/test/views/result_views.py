from rest_framework import mixins, viewsets, permissions
from ..models import ResultsTest
from ..serializers import ResultsTestSerializer, ResultsTestCreateSerializer


class ResultsTestViewSet(
    mixins.CreateModelMixin,   # POST /api/results/
    mixins.ListModelMixin,     # GET /api/results/
    mixins.RetrieveModelMixin, # GET /api/results/{id}/
    viewsets.GenericViewSet
):

    queryset = ResultsTest.objects.all().select_related("test", "test__level")
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return ResultsTestCreateSerializer
        return ResultsTestSerializer
