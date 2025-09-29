from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Post, Category, Tag
from .serializers import PostSerializer, CategorySerializer, TagSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            description='Поиск по названию',
            required=False,
            type=str
        )
    ]
)
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('title')
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            description='Поиск по названию',
            required=False,
            type=str
        )
    ]
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('title')
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с Post
    Поддерживает фильтрацию по ?term=
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='term',
                description='Фильтрация по заголовку, контенту или категории',
                required=False,
                type=str
            )
        ]
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        term = self.request.query_params.get('term', None)
        if term:
            queryset = queryset.filter(
                Q(title__icontains=term) |
                Q(content__icontains=term) |
                Q(category__title__icontains=term)
            ).distinct()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response(PostSerializer(post).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


