from celery import shared_task
from django.utils import timezone
from .models import Task
from django.conf import settings
import requests

@shared_task
def send_task_reminders():
    now = timezone.now()
    tasks = Task.objects.filter(done=False, due_date__lte=now)

    for task in tasks:
        user = task.owner
        if user.telegram_id:
            message = (
                f"⚡ Напоминание!\n"
                f"Задача: {task.title}\n"
                f"Описание: {task.description or '—'}\n"
                f"Дата выполнения: {task.due_date.strftime('%d.%m.%Y %H:%M')}"
            )
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            try:
                requests.post(url, data={"chat_id": user.telegram_id, "text": message})
            except Exception as e:
                print(f"Ошибка отправки уведомления: {e}")
