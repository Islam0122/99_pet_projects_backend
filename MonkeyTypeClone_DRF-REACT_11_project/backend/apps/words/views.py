from rest_framework import viewsets
from rest_framework import filters
from .models import Timer, Category, Text
from .serializers import TimerSerializer, CategorySerializer, TextSerializer
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(tags=["⏱ Timers"])
class TimerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Timer.objects.all()
    serializer_class = TimerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['seconds']

    @extend_schema(
        summary="Получить список таймеров",
        description="Возвращает список таймеров. Поиск доступен по `seconds`.",
        parameters=[
            OpenApiParameter(name="search", description="Поиск по секундам", required=False, type=int),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["📂 Categories"])
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @extend_schema(
        summary="Список категорий",
        description="Возвращает список категорий. Можно искать по `name`.",
        parameters=[
            OpenApiParameter(name="search", description="Поиск по названию", required=False, type=str),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["📝 Texts"])
class TextViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['text_content']
    filterset_fields = ['category']

    @extend_schema(
        summary="Список текстов",
        description="Возвращает список текстов. Доступен поиск по содержимому текста и фильтрация по категории.",
        parameters=[
            OpenApiParameter(name="search", description="Поиск по тексту", required=False, type=str),
            OpenApiParameter(name="category", description="Фильтр по категории", required=False, type=int),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
