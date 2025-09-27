import aiohttp
from datetime import datetime
from config.config import load_config
from lexicon.lexicon_ru import LEXICON_RU
from lexicon.lexicon_en import LEXICON_EN
from .redis_client import RedisClient

import json

config = load_config()
BASE_URL = f"{config.api_url.api_url}/tg-users/"
HEADERS = {"Content-Type": "application/json"}
REDIS_TTL = 120

class TgUserAPI:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = HEADERS
        self.session = None
        self.redis_client = RedisClient()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        await self.redis_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        await self.redis_client.__aexit__(exc_type, exc_val, exc_tb)

    async def get_user_by_telegram_id(self, telegram_id: int):
        cache_key = f"tg_user:{telegram_id}"
        cached = await self.redis_client.get(cache_key)
        if cached:
            return cached

        url = f"{self.base_url}?telegram_id={telegram_id}"
        async with self.session.get(url, headers=self.headers) as resp:
            resp.raise_for_status()
            data = await resp.json()
            results = data.get("results", [])
            user = results[0] if results else None
            if user:
                await self.redis_client.set(cache_key, user)
            return user

    async def create_or_update_user(self, username: str, full_name: str, telegram_id: int, language: str = "ru"):
        user = await self.get_user_by_telegram_id(telegram_id)
        if user:
            data_to_update = {
                "username": username,
                "full_name": full_name,
                "language": language,
                "joined_at": datetime.utcnow().isoformat()
            }
            url = f"{self.base_url}{user['id']}/"
            async with self.session.patch(url, json=data_to_update, headers=self.headers) as resp:
                resp.raise_for_status()
                updated_user = await resp.json()
                await self.redis_client.set(f"tg_user:{telegram_id}", updated_user)
                return updated_user
        else:
            payload = {
                "username": username,
                "full_name": full_name,
                "telegram_id": telegram_id,
                "language": language
            }
            async with self.session.post(self.base_url, json=payload, headers=self.headers) as resp:
                resp.raise_for_status()
                new_user = await resp.json()
                await self.redis_client.set(f"tg_user:{telegram_id}", new_user)
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
