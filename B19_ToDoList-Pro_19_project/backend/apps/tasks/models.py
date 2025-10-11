from django.db import models
from ..utils.snowflake import next_id
from ..accounts.models import TGUser


class SnowflakePK(models.BigIntegerField):
    """Кастомное поле для генерации Snowflake ID вместо стандартных PK."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("primary_key", True)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if add and not value:
            value = next_id()
            setattr(model_instance, self.attname, value)
        return value


class Category(models.Model):
    """Категории (теги) для задач."""
    id = SnowflakePK()
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Название категории",
        help_text="Введите уникальное название категории"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Task(models.Model):
    """Модель задачи ToDo."""
    id = SnowflakePK()
    title = models.CharField(
        max_length=255,
        verbose_name="Название задачи",
        help_text="Введите короткое название задачи"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание задачи",
        help_text="Можно указать дополнительные детали задачи"
    )
    owner = models.ForeignKey(
        TGUser,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Владелец"
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="tasks",
        verbose_name="Категории"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата выполнения"
    )
    done = models.BooleanField(
        default=False,
        verbose_name="Выполнено",
        help_text="Отметьте, если задача завершена"
    )
    created_reminder_sent = models.BooleanField(
        default=False,
        verbose_name="Напоминание о создании отправлено"
    )
    due_reminder_sent = models.BooleanField(
        default=False,
        verbose_name="Напоминание о дедлайне отправлено"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title
