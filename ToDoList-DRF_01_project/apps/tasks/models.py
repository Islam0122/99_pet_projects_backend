import uuid
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


class Task(BaseModel):
    class Status(models.TextChoices):
        CREATED = "created", "Создано"
        IN_PROGRESS = "in_progress", "В работе"
        COMPLETED = "completed", "Завершено"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID задачи",
        help_text="Уникальный идентификатор задачи"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Название задачи",
        help_text="Краткое название задачи (до 255 символов)"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание задачи",
        help_text="Подробное описание задачи (может быть пустым)"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
        verbose_name="Статус задачи",
        help_text="Текущий статус задачи"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Время, когда задача была создана"
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["-created_at"]  # последние сверху

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
