import requests
from django.conf import settings

def notify_telegram(text: str):
    if not getattr(settings, "TELEGRAM_NOTIFY_ENABLED", False):
        return

    token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", None)
    if not token or not chat_id:
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})
    except Exception:
        pass
