from celery import shared_task
from django.utils import timezone
from .models import Task
from django.conf import settings
import requests

@shared_task
def send_task_reminders():
    now = timezone.now()

    new_tasks = Task.objects.filter(done=False, created_reminder_sent=False)
    for task in new_tasks:
        if task.owner.telegram_id:
            message = (
                f"✅ Твоя задача создана!\n"
                f"Задача: {task.title}\n"
                f"Описание: {task.description or '—'}\n"
                f"Дата выполнения: {task.due_date.strftime('%d.%m.%Y %H:%M') if task.due_date else '—'}"
            )
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            try:
                requests.post(url, data={"chat_id": task.owner.telegram_id, "text": message})
                task.created_reminder_sent = True
                task.save(update_fields=["created_reminder_sent"])
            except Exception as e:
                print(f"Ошибка при уведомлении о создании: {e}")

    reminder_time = now + timezone.timedelta(minutes=15)
    due_tasks = Task.objects.filter(
        done=False,
        due_date__gte=now,  # только будущие или текущие задачи
        due_date__lte=reminder_time,
        due_reminder_sent=False
    )
    for task in due_tasks:
        if task.owner.telegram_id:
            message = (
                f"⚡ Внимание! Твоя задача скоро заканчивается!\n"
                f"Задача: {task.title}\n"
                f"Описание: {task.description or '—'}\n"
                f"Дата выполнения: {task.due_date.strftime('%d.%m.%Y %H:%M')}"
            )
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            try:
                requests.post(url, data={"chat_id": task.owner.telegram_id, "text": message})
                task.due_reminder_sent = True
                task.save(update_fields=["due_reminder_sent"])
            except Exception as e:
                print(f"Ошибка при уведомлении о дедлайне: {e}")
