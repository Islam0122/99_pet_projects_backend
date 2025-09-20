from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API для категорий рецептов.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
