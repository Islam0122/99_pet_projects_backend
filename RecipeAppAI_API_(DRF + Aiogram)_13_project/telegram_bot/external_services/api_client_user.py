import aiohttp
from datetime import datetime
from config.config import load_config
from lexicon.lexicon_ru import LEXICON_RU
from lexicon.lexicon_en import LEXICON_EN

config = load_config()
BASE_URL = f"{config.api_url.api_url}/tg-users/"
HEADERS = {"Content-Type": "application/json"}


class TgUserAPI:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_tg_users(self):
        async with self.session.get(self.base_url, headers=self.headers) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def create_tg_user(self, username, full_name, telegram_id, language="ru"):
        payload = {
            "username": username,
            "full_name": full_name,
            "telegram_id": telegram_id,
            "language": language
        }
        async with self.session.post(self.base_url, json=payload, headers=self.headers) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def update_tg_user(self, user_id, data: dict):
        url = f"{self.base_url}{user_id}/"
        async with self.session.patch(url, json=data, headers=self.headers) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def delete_tg_user(self, user_id):
        url = f"{self.base_url}{user_id}/"
        async with self.session.delete(url, headers=self.headers) as resp:
            return resp.status

    async def get_user_by_telegram_id(self, telegram_id: int):
        url = f"{self.base_url}?telegram_id={telegram_id}"
        async with self.session.get(url, headers=self.headers) as resp:
            resp.raise_for_status()
            data = await resp.json()
            results = data.get("results", [])
            return results[0] if results else None

    async def create_or_update_user(self, username: str, full_name: str, telegram_id: int, language: str = "ru"):
        existing_user = await self.get_user_by_telegram_id(telegram_id)

        if existing_user:
            data_to_update = {
                "username": username,
                "full_name": full_name,
                "language": language,
                "joined_at": datetime.utcnow().isoformat()
            }
            updated_user = await self.update_tg_user(existing_user["id"], data_to_update)
            return updated_user
        else:
            new_user = await self.create_tg_user(username, full_name, telegram_id, language)
            return new_user

    async def get_user_lexicon(self, telegram_id: int):
        try:
            user = await self.get_user_by_telegram_id(telegram_id)
            if not user:
                return LEXICON_RU
            language = user.get("language", "ru").lower()
            return LEXICON_EN if language == "en" else LEXICON_RU
        except Exception:
            return LEXICON_RU
