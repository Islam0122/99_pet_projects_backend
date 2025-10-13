from django.db import models
from django.utils import timezone


class TGUser(models.Model):
    telegram_id = models.CharField(
        max_length=120,
        unique=True,
        verbose_name="Telegram ID"
    )
    username = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Имя пользователя"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )

    xp = models.IntegerField(default=0, verbose_name="Опыт (XP)")
    total_read_books = models.IntegerField(default=0, verbose_name="Прочитано книг")
    streak_days = models.IntegerField(default=0, verbose_name="Серия дней подряд")
    last_read_date = models.DateField(blank=True, null=True, verbose_name="Последнее чтение")
    last_active = models.DateTimeField(default=timezone.now, verbose_name="Последняя активность")

    level = models.IntegerField(default=1, verbose_name="Уровень")
    rank = models.CharField(
        max_length=50,
        default="Новичок",
        verbose_name="Звание",
        help_text="Например: Новичок, Читатель, Мастер чтения"
    )
    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"

    def __str__(self):
        return f"{self.username or self.telegram_id} — {self.streak_days} дней подряд"

    def add_xp(self, amount: int):
        """Добавляет опыт и повышает уровень при достижении порога"""
        self.xp += amount
        if self.xp >= self.level * 100:
            self.level += 1
            self.rank = self.get_rank_name()
        self.save()

    def get_rank_name(self):
        """Возвращает звание в зависимости от уровня"""
        if self.level < 5:
            return "Новичок"
        elif self.level < 10:
            return "Читатель"
        elif self.level < 20:
            return "Книжный мастер"
        else:
            return "Легенда чтения"

    def update_activity(self):
        """Обновляет дату последней активности"""
        self.last_active = timezone.now()
        self.save()
