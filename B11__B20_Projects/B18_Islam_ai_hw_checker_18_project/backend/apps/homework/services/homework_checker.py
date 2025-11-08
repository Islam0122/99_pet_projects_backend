import uuid
import json
import requests
from requests.auth import HTTPBasicAuth
import re

CLIENT_ID = '71b92890-bf91-4b6b-9645-6561b93e3d7d'
SECRET = '3278c7e4-6c0c-4b7b-a8b7-9baadb679504'



def get_access_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),  # уникальный идентификатор запроса
    }
    payload = {"scope": "GIGACHAT_API_PERS"}

    try:
        res = requests.post(
            url=url,
            headers=headers,
            auth=HTTPBasicAuth(CLIENT_ID, SECRET),
            data=payload,
            verify=False,  # Убедитесь, что использование verify=False безопасно для вашей среды
        )
        res.raise_for_status()  # проверка на наличие ошибок
        access_token = res.json().get("access_token")
        if not access_token:
            raise ValueError("Токен доступа не был получен.")
        return access_token
    except requests.RequestException as e:
        print("Ошибка при получении access token:", e)
        return None


def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat",
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": msg,
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        response.raise_for_status()  # проверка на наличие ошибок
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        print("Ошибка при отправке запроса к GigaChat API:", e)
        return "Ошибка при получении ответа от GigaChat."


def sent_prompt_and_get_response(msg: str):
    access_token = get_access_token()
    message = msg
    if access_token:
        response = send_prompt(message, access_token)
        decorated_response = f'{response}'
        return decorated_response
    else:
        return "Не удалось получить access token."
    
    
def extract_grade_from_feedback(feedback_text: str):
    # Ищем шаблон цифры перед "/10", например "6/10"
    match = re.search(r'(\d+(\.\d+)?)\s*/\s*10', feedback_text)
    if match:
        return float(match.group(1))
    return None
