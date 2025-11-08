from rest_framework import viewsets
from rest_framework import filters
from .models import Timer, Category, Text
from .serializers import TimerSerializer, CategorySerializer, TextSerializer
from django_filters.rest_framework import DjangoFilterBackend

class TimerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['seconds']

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class TextViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['text_content']
    filterset_fields = ['category']