import aiohttp
import logging
from typing import Optional, List
from config.config import load_config

logger = logging.getLogger(__name__)
config = load_config()
API_URL = f"{config.api_url.api_url}"



async def get_telegram_users() -> List[dict]:
    """Получение всех Telegram-пользователей"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/telegram-users/") as resp:
            resp.raise_for_status()
            return await resp.json()


async def get_telegram_user(user_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/telegram-users?telegram_id={user_id}") as resp:
            resp.raise_for_status()
            users = await resp.json()
            if not users:
                return {}
            return users[0]



async def create_or_update_telegram_user(tg_id: int, username: str):
    async with aiohttp.ClientSession() as session:
        url = f"{config.api_url.api_url}/telegram-users/"
        payload = {"telegram_id": tg_id, "username": username or ""}

        async with session.post(url, json=payload) as resp:
            if resp.status == 201:
                return await resp.json()  # создан новый пользователь
            elif resp.status == 400:
                async with session.patch(url, json=payload) as resp2:
                    resp2.raise_for_status()
                    return await resp2.json()

async def delete_telegram_user(user_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{API_URL}/telegram-users/{user_id}/") as resp:
            resp.raise_for_status()
            return {"status": "deleted", "user_id": user_id}