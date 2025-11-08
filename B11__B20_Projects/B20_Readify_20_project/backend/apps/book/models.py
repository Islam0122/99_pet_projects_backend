from django.db import models
from ..accounts.models import TGUser


class Book(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название книги",
        help_text="Введите название книги"
    )
    author = models.CharField(
        max_length=255,
        verbose_name="Автор",
        help_text="Введите имя автора книги"
    )
    total_chapters = models.IntegerField(
        default=0,
        verbose_name="Количество глав",
        help_text="Общее количество глав в книге"
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['title']

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(
        Book,
        related_name="chapters",
        on_delete=models.CASCADE,
        verbose_name="Книга",
        help_text="Выберите книгу, к которой относится эта глава"
    )
    number = models.IntegerField(
        verbose_name="Номер главы",
        help_text="Введите номер главы"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Название главы",
        help_text="Введите название главы"
    )
    text = models.TextField(
        verbose_name="Текст главы",
        help_text="Введите текст главы"
    )

    class Meta:
        verbose_name = "Глава"
        verbose_name_plural = "Главы"
        ordering = ['book', 'number']

    def __str__(self):
        return f"{self.book.title} — Глава {self.number}"


class UserBook(models.Model):
    telegram_user = models.ForeignKey(
        TGUser,
        on_delete=models.CASCADE,
        related_name="user_books",
        verbose_name="Пользователь",
        help_text="Пользователь, который добавил книгу"
    )

    title = models.CharField(
        max_length=255,
        verbose_name="Название книги",
        help_text="Введите название вашей книги"
    )

    description = models.TextField(
        verbose_name="Описание книги",
        help_text="Кратко опишите, о чём книга"
    )

    file = models.FileField(
        upload_to="user_books/files/",
        verbose_name="Файл книги (PDF, TXT и др.)",
        help_text="Загрузите файл книги"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления",
        help_text="Когда книга была добавлена пользователем"
    )

    class Meta:
        verbose_name = "Книга пользователя"
        verbose_name_plural = "Книги пользователей"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.telegram_user.username or self.telegram_user.telegram_id}"
