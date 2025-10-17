from rest_framework import serializers
from .models import Book, Chapter

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['number', 'title', 'text']
        extra_kwargs = {
            'number': {'help_text': 'Номер главы'},
            'title': {'help_text': 'Название главы'},
            'text': {'help_text': 'Текст главы'},
        }


class BookSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'total_chapters', 'chapters']
        extra_kwargs = {
            'title': {'help_text': 'Название книги'},
            'author': {'help_text': 'Автор книги'},
            'total_chapters': {'help_text': 'Общее количество глав в книге', 'read_only': True},
        }
