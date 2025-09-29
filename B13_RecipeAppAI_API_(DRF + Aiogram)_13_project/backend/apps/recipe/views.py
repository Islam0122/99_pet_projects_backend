from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe
from .serializers import RecipeSerializer

class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Фильтры
    filterset_fields = ['category']          # фильтрация по category_id
    search_fields = ['title', 'ingredients'] # поиск по названию и ингредиентам
    ordering_fields = ['created_at', 'title'] # сортировка по дате создания или названию
    ordering = ['title']                      # дефолтная сортировка
