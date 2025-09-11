from django.conf import settings
from django.db import models
from django.db.models import Max, Avg
from ..words.models import Timer,Category

class TestResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="test_results"
    )
    wpm = models.FloatField(verbose_name="Words Per Minute")
    accuracy = models.FloatField(verbose_name="Accuracy %")
    timer = models.ForeignKey(
        Timer,
        on_delete=models.SET_NULL,
        null=True,
        related_name="test_results",
        verbose_name="Таймер"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="test_results",
        verbose_name="Категория"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.user:
            agg = TestResult.objects.filter(user=self.user).aggregate(
                best_wpm=Max('wpm'),
                avg_accuracy=Avg('accuracy')
            )
            self.user.best_wpm = agg['best_wpm'] or 0
            self.user.average_accuracy = agg['avg_accuracy'] or 0
            self.user.save()

    def __str__(self):
        seconds = self.timer.seconds if self.timer else "N/A"
        return f"{self.user} - {self.wpm} WPM ({seconds}s)"
