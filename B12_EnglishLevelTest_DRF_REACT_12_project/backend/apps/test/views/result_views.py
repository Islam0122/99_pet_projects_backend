from rest_framework import permissions
from ..models import ResultsTest,PlacementTestResult
from ..serializers import ResultsTestSerializer, ResultsTestCreateSerializer, PlacementTestResultSerializer, \
    PlacementTestResultCreateSerializer, PlacementTestSerializer
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response


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

class PlacementTestResultViewSet(viewsets.GenericViewSet,
                                 mixins.CreateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin):
    queryset = PlacementTestResult.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return PlacementTestResultCreateSerializer
        return PlacementTestResultSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        # Возвращаем полный сериализатор с рассчитанными полями
        full_serializer = PlacementTestResultSerializer(instance, context={'request': request})
        return Response(full_serializer.data, status=status.HTTP_201_CREATED)