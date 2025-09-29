from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Tag, Quote
from .serializers import AuthorSerializer, TagSerializer, QuoteSerializer, QuoteCreateSerializer
from .filters import QuoteFilter


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuoteFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return QuoteSerializer  # read (вложенные данные)
        return QuoteCreateSerializer  # write (id)
