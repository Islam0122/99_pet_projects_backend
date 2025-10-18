from rest_framework import serializers
from .models import Book, Chapter, UserBook

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


class UserBookSerializer(serializers.ModelSerializer):
    telegram_username = serializers.CharField(
        source="telegram_user.username",
        read_only=True
    )
    telegram_id = serializers.IntegerField(
        source="telegram_user.telegram_id",
        read_only=True
    )

    class Meta:
        model = UserBook
        fields = [
            "id",
            "title",
            "description",
            "file",
            "telegram_user",
            "telegram_username",
            "telegram_id",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]