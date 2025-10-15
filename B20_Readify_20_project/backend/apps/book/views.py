from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from bs4 import BeautifulSoup

class LibRuBookView(APIView):
    def get(self, request):
        url = request.query_params.get("url")
        if not url:
            return Response({"error": "Не указан URL"}, status=status.HTTP_400_BAD_REQUEST)

        url = url.strip()  # убираем лишние пробелы и переносы

        try:
            resp = requests.get(url)
            resp.raise_for_status()
            resp.encoding = 'cp1251'  # обязательно для Lib.ru
        except requests.RequestException:
            return Response({"error": "Не удалось получить страницу"}, status=status.HTTP_404_NOT_FOUND)

        # Парсим текст
        soup = BeautifulSoup(resp.text, "html.parser")
        pre_tag = soup.find("pre")  # книги в <pre>
        text = pre_tag.get_text() if pre_tag else soup.get_text()

        lines = [line.strip() for line in text.splitlines() if line.strip()]

        return Response({
            "url": url,
            "lines_count": len(lines),
            "lines": lines[:100]  # первые 100 строк для примера
        })
