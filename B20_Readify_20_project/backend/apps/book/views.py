from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Book, Chapter
from .serializers import BookSerializer, ChapterSerializer
from .utils import load_book_from_openlibrary
from ..accounts.models import TGUser


class BookListAPIView(APIView):
    """Список всех книг, сортировка по названию"""
    def get(self, request):
        books = Book.objects.all().order_by('title')
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)



class ChapterDetailAPIView(APIView):
    """Получение конкретной главы книги по номеру"""
    def get(self, request, book_id, chapter_number):
        chapter = get_object_or_404(Chapter.objects.select_related('book'),
                                    book_id=book_id, number=chapter_number)
        serializer = ChapterSerializer(chapter)
        return Response(serializer.data)


class LoadBookAPIView(APIView):
    """Авто-добавление книги через OLID (если нет — создаётся)"""
    def post(self, request):
        olid = request.data.get("olid")
        if not olid:
            return Response({"error": "Не указан OLID"}, status=status.HTTP_400_BAD_REQUEST)

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
