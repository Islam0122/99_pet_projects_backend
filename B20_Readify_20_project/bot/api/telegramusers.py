import aiohttp
import logging
from typing import List, Optional
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


async def get_telegram_user(tg_id: int) -> Optional[dict]:
    """Получение одного пользователя по telegram_id"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/telegram-users/{tg_id}/") as resp:
            if resp.status == 404:
                return None
            resp.raise_for_status()
            return await resp.json()


async def create_or_update_telegram_user(tg_id: int, username: str) -> dict:
    """Создание или обновление пользователя"""
    async with aiohttp.ClientSession() as session:
        url = f"{API_URL}/telegram-users/"
        payload = {"telegram_id": tg_id, "username": username or ""}

        async with session.post(url, json=payload) as resp:
            resp.raise_for_status()
            return await resp.json()


async def add_xp_to_user(tg_id: int, xp_amount: int) -> dict:
    """
    Добавление XP пользователю.
    Серия дней, уровень и звание обновляются автоматически через сериалайзер.
    """
    user = await get_telegram_user(tg_id)
    if not user:
        raise ValueError(f"Пользователь {tg_id} не найден")

    new_xp = user.get("xp", 0) + xp_amount
    async with aiohttp.ClientSession() as session:
        url = f"{API_URL}/telegram-users/{tg_id}/"
        payload = {"xp": new_xp}

        async with session.patch(url, json=payload) as resp:
            resp.raise_for_status()
            return await resp.json()


async def get_top_users(limit: int = 10) -> List[dict]:
    """Получение топ-10 пользователей по XP"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/telegram-top/") as resp:
            resp.raise_for_status()
            users = await resp.json()
            return users[:limit]


async def delete_telegram_user(tg_id: int) -> dict:
    """Удаление пользователя"""
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{API_URL}/telegram-users/{tg_id}/") as resp:
            resp.raise_for_status()
            return {"status": "deleted", "telegram_id": tg_id}
