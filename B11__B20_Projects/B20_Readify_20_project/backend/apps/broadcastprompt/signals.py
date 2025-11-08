import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import BroadcastPrompt
from ..accounts.models import TGUser as TgUser
import os

BOT_TOKEN = "8207304587:AAER_XWqQPgthD6Uf3iZrakevE_IFxwb7R8"

def send_prompt_to_all_users(prompt_text,title):
    users = TgUser.objects.all()
    for user in users:
        if not user.telegram_id:
            continue
        text = f"""
        ✨Readify ✨  
        📌 {title}  
        {prompt_text}  
        """
        payload = {
            "chat_id": user.telegram_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json=payload)
            response.raise_for_status()
            print(f"Сообщение отправлено пользователю {user.telegram_id}")
        except requests.RequestException as e:
            print(f"Ошибка при отправке пользователю {user.telegram_id}: {e}")

@receiver(post_save, sender=BroadcastPrompt)
def broadcast_prompt_post_save(sender, instance, created, **kwargs):
    if created and not instance.is_sent:
        send_prompt_to_all_users(instance.prompt_text,instance.title)
        instance.is_sent = True
        instance.sent_at = timezone.now()
        instance.save()
