import requests
from django.conf import settings

def send_otp(mobile, otp):
    """
    Send OTP via Infobip API.
    """
    # Убедитесь, что base_api и API_KEY настроены в settings.py
    base_url = f"https://{settings.INFOBIP_BASE_API}/sms/2/text/advanced"
    api_key = settings.INFOBIP_API_KEY

    headers = {
        'Authorization': f'App {api_key}',
        'Content-Type': 'application/json',
    }

    payload = {
        "messages": [
            {
                "from": "ServiceSMS",
                "destinations": [{"to": mobile}],
                "text": f"🔐 Ваш код для подтверждения: {otp}\n\n"
                        f"Этот код был отправлен вам от Дуйшобаев Ислам.\n\n"
                        f"⏳ Пожалуйста, введите его в течение 10 минут для завершения регистрации."
            }
        ]
    }

    # Отправка POST запроса на Infobip API
    response = requests.post(base_url, json=payload, headers=headers)

    # Проверка ответа
    if response.status_code == 200:
        return True
    else:
        return False
