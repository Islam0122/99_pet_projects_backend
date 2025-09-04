import uuid
from django.db import models
from django.core.exceptions import ValidationError


class FairyTale(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Уникальный идентификатор"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Название сказки",
        help_text="Введите заголовок сказки (до 255 символов)."
    )
    story = models.TextField(
        verbose_name="История",
        help_text="Введите полный текст сказки."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата автоматически проставляется при добавлении сказки."
    )

    class Meta:
        verbose_name = "Сказка"
        verbose_name_plural = "Сказки"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
