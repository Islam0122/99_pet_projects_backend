from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Book, Chapter, UserBook
from .serializers import BookSerializer, ChapterSerializer, UserBookSerializer
from .utils import load_book_from_openlibrary
from ..accounts.models import TGUser


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    """📚 Управление книгами"""
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'author']

    @action(detail=True, methods=['get'])
    def chapters(self, request, pk=None):
        """📖 Получить все главы книги"""
        book = self.get_object()
        chapters = book.chapters.all().order_by('number')
        serializer = ChapterSerializer(chapters, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def chapter(self, request, pk=None, chapter_number=None):
        """📖 Получить конкретную главу"""
        book = self.get_object()
        chapter = get_object_or_404(Chapter, book=book, number=chapter_number)
        serializer = ChapterSerializer(chapter)
        return Response(serializer.data)


class ChapterViewSet(viewsets.ReadOnlyModelViewSet):
    """📖 Управление главами"""
    queryset = Chapter.objects.all().select_related('book').order_by('book__title', 'number')
    serializer_class = ChapterSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book']


class BookListAPIView(APIView):
    """📚 Список всех книг"""

    def get(self, request):
        books = Book.objects.all().order_by('title')
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class ChapterDetailAPIView(APIView):
    """📖 Получение конкретной главы книги по номеру"""

    def get(self, request, book_id, chapter_number):
        chapter = get_object_or_404(
            Chapter.objects.select_related('book'),
            book_id=book_id,
            number=chapter_number
        )
        serializer = ChapterSerializer(chapter)
        return Response(serializer.data)


class LoadBookAPIView(APIView):
    """🔄 Загрузка книги по OLID (через OpenLibrary API)"""

    def post(self, request):
        olid = request.data.get("olid")
        if not olid:
            return Response({"error": "Не указан OLID"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, есть ли уже книга
        book = Book.objects.filter(title=olid).first()
        if book:
            serializer = BookSerializer(book)
            return Response(serializer.data)

        try:
            book = load_book_from_openlibrary(olid)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserBookViewSet(viewsets.ModelViewSet):
    queryset = UserBook.objects.all().order_by("-created_at")
    serializer_class = UserBookSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["get"])
    def read_file(self, request, pk=None):
        book = self.get_object()

        if not book.file:
            return Response({"error": "Файл не найден"}, status=status.HTTP_404_NOT_FOUND)

        try:
            with open(book.file.path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            numbered_lines = [
                f" {line.strip()}"
                for i, line in enumerate(lines)
                if line.strip()
            ]
            content = "\n".join(numbered_lines)

            return Response({
                "title": book.title,
                "content": content
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "📘 Книга успешно добавлена!", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )
