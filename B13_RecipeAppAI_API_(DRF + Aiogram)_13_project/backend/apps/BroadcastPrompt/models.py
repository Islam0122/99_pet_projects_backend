from django.db import models

class BroadcastPrompt(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок рассылки")
    prompt_text = models.TextField(verbose_name="Текст или промпт")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата отправки")
    is_sent = models.BooleanField(default=False, verbose_name="Отправлено")

    class Meta:
        db_table = "broadcast_prompt"
        verbose_name = "рассылки"
        verbose_name_plural = "рассылки"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
