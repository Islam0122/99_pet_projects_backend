from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .utils import find_chapter_by_number
import re

class QueryBookView(APIView):
    """
    API для поиска текста книги по главе
    """

    def post(self, request):
        book_title = request.data.get("book_title")
        query = request.data.get("query")

        if not book_title or not query:
            return Response({"error": "Нужно указать 'book_title' и 'query'"}, status=400)

        try:
            book = Book.objects.get(title__icontains=book_title)
        except Book.DoesNotExist:
            return Response({"error": "Книга не найдена"}, status=404)

        # Ищем номер главы из запроса
        match = re.search(r'(\d+)', query)
        if match:
            chapter_num = int(match.group(1))
            chapter_text = find_chapter_by_number(book.text, chapter_num)
            if chapter_text:
                return Response({
                    "book": book.title,
                    "chapter_number": chapter_num,
                    "chapter_text": chapter_text[:2000] + "..." if len(chapter_text) > 2000 else chapter_text
                })
            else:
                return Response({"error": "Глава не найдена"}, status=404)

        return Response({"error": "Не удалось понять запрос"}, status=400)
