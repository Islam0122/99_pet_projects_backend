from django.shortcuts import render
from rest_framework import viewsets
from .serializers import CategorySerializer, ProductSerializer
from .models import Category, Product
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from rest_framework.decorators import action

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ["is_archived", "category", "created_at", "updated_at"]
    search_fields = ["title", "identification_number", "category__title"]

    @extend_schema(
        responses=OpenApiResponse(
            description="Архивирование/Восстановление товара",
            examples=[
                {"detail": "Товар архивирован"},
                {"detail": "Товар восстановлен"}
            ]
        )
    )
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_archived = not product.is_archived
        product.save()
        return Response(
            {"detail": f"Товар {'архивирован' if product.is_archived else 'восстановлен'}"},
            status=status.HTTP_200_OK
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(name="is_archived", description="Фильтр по архиву", required=False, type=bool),
            OpenApiParameter(name="category", description="ID категории", required=False, type=int),
            OpenApiParameter(name="created_at", description="Дата создания", required=False, type=str),
            OpenApiParameter(name="updated_at", description="Дата обновления", required=False, type=str),
        ],
        responses=ProductSerializer,
        description="Список товаров с фильтрацией и поиском"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

