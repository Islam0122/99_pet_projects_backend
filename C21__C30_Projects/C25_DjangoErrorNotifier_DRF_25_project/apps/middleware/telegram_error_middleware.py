import requests
import traceback
from django.conf import settings
from apps.utils.gigachat import sent_prompt_and_get_response

class TelegramErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Отправка всех ошибок HTTP >=400
        emoji = "🔥" if response.status_code >= 500 else "⚠️"
        text = (
                f"{emoji} <b>Django Error Report</b>\n"
                f"👤 Пользователь: {getattr(request, 'user', 'Anonymous')}\n"
                f"🌐 URL: {request.path}\n"
                f"📌 Метод: {request.method}\n"
                f"💻 Код ошибки: {response.status_code}\n"
            )
        if response.status_code == 500:
                text += f"<pre>{traceback.format_exc()}</pre>"

            # Отправляем текст ошибки в Telegram
        self.send_telegram(text)

            # Получаем совет от GigaChat
        advice = sent_prompt_and_get_response(f"Ислам, вот ошибка в Django:\n{text}\nДай совет, как её исправить.")
        if advice:
            self.send_telegram(f"💡 <b>Совет от GigaChat:</b>\n{advice}")
        return response

    @staticmethod
    def send_telegram_static(text: str):
        token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
        chat_id = getattr(settings, "TELEGRAM_CHAT_ID", None)
        if not token or not chat_id:
            print("Telegram токен или чат не настроен")
            return
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
                timeout=5
            )
        except Exception as e:
            print("Ошибка при отправке в Telegram:", e)

    def process_exception(self, request, exception):
        if not getattr(settings, "TELEGRAM_NOTIFY_ENABLED", False):
            return None

        text = (
            "🔥 Django Exception Alert\n"
            f"👤 Пользователь: {getattr(request, 'user', 'Anonymous')}\n"
            f"🌐 URL: {request.path}\n"
            f"📌 Метод: {request.method}\n"
            f"⚠️ Exception: {exception}\n\n"
            f"<pre>{traceback.format_exc()}</pre>"
        )

        # Отправляем ошибку в Telegram
        self.send_telegram(text)

        prompt = f"""
       Ты Django разработчик. 
Я, Islam Dev, получил следующую ошибку в проекте:

{text}

❓ Проанализируй её и дай:
1. Короткое объяснение причины ошибки.
2. Конкретный совет, как исправить.
⚡ Ответ должен быть кратким, понятным и структурированным, чтобы можно было сразу применить.

❌ Не присылай код, Docker, файлы или структуру проекта. Только объяснение и совет.
 """

        advice = sent_prompt_and_get_response(prompt)
        if advice:
            self.send_telegram(f"💡 <b>Совет :</b>\n{advice}")

        return None

    def send_telegram(self, text: str):
        token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
        chat_id = getattr(settings, "TELEGRAM_CHAT_ID", None)
        if not token or not chat_id:
            print("Telegram токен или чат не настроен")
            return
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
                timeout=5
            )
        except Exception as e:
            print("Ошибка при отправке в Telegram:", e)
