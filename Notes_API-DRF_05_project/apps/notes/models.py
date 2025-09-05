import uuid
from django.conf import settings
from django.db import models

class Note(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Уникальный идентификатор",
        help_text="Уникальный UUID для каждой заметки."
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        help_text="Введите заголовок заметки (до 255 символов)."
    )
    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Введите текст заметки."
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="notes",
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        help_text="Пользователь, которому принадлежит эта заметка."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время, когда заметка была создана."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Дата и время последнего изменения заметки."
    )

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
