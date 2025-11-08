import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        abstract = True


class Link(BaseModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID ссылки"
    )
    original_url = models.URLField(
        max_length=255,
        unique=True,
        verbose_name="Оригинальная ссылка",
        help_text="Введите полный URL, который нужно сократить"
    )
    short_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Короткий код",
        help_text="Автоматически генерируемый код длиной 6–10 символов"
    )
    clicks = models.IntegerField(
        default=0,
        verbose_name="Количество переходов",
        help_text="Сколько раз по этой ссылке переходили"
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата истечения",
        help_text="Если указана, ссылка перестанет работать после этой даты"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна"
    )

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=15)
        self.is_active = self.expires_at > timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        return self.expires_at is None or self.expires_at > timezone.now()

    class Meta:
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.short_code} → {self.original_url}"

