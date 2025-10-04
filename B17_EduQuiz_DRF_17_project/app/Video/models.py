from django.db import models

class VideoCategory(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название категории",
        help_text="Введите название категории видео"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория видео"
        verbose_name_plural = "Категории видео"

class Video(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название видео",
        help_text="Введите название видео"
    )
    description = models.TextField(  # Новое поле
        verbose_name="Описание видео",
        help_text="Добавьте краткое описание видео",
        blank=True,  # Поле необязательно
        null=True
    )
    video_category = models.ForeignKey(
        VideoCategory,
        on_delete=models.CASCADE,
        related_name="videos",
        verbose_name="Категория видео",
        help_text="Выберите категорию для видео"
    )
    video_url = models.URLField(
        verbose_name="URL видео",
        help_text="Введите ссылку на YouTube видео"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время добавления видео"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активно",
        help_text="Установите в False, чтобы деактивировать видео"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
