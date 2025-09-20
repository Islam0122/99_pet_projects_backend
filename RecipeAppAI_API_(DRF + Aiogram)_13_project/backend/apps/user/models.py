from django.db import models

class TgUser(models.Model):
    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Юзернейм",
        help_text="Уникальное имя пользователя в Telegram (@username)"
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name="Полное имя",
        help_text="Полное имя пользователя из профиля Telegram"
    )
    telegram_id = models.CharField(
        max_length=255,
        verbose_name="Telegram ID",
        help_text="Уникальный идентификатор пользователя в Telegram"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
        help_text="Дата и время создания записи"
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата присоединения",
        help_text="Когда пользователь впервые начал пользоваться ботом"
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Telegram пользователь"
        verbose_name_plural = "Telegram пользователи"
        ordering = ['-created_at']
