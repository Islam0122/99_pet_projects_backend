from django.db import models
from django.utils import timezone

class TGUser(models.Model):
    telegram_id = models.CharField(max_length=120, unique=True)
    username = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_task_completes = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    last_task_completed = models.DateTimeField(blank=True, null=True)

    def update_streak(self):
        today = timezone.now().date()
        if self.last_task_completed:
            last_date = self.last_task_completed.date()
            if (today - last_date).days == 1:
                self.streak_days += 1
            elif (today - last_date).days > 1:
                self.streak_days = 1
        else:
            self.streak_days = 1
        self.last_task_completed = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.username or self.telegram_id} — {self.streak_days} дней подряд"
