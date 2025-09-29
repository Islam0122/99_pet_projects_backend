from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Table
from .serializers import TableSerializer

class TableViewSet(ReadOnlyModelViewSet):
    """
    Просмотр списка столиков.
    Поддерживает фильтрацию по id, дате создания, дате обновления и локации.
    """
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'created_at', 'updated_at', 'location']
    ordering_fields = ['number', 'capacity', 'created_at']
    ordering = ['number']
