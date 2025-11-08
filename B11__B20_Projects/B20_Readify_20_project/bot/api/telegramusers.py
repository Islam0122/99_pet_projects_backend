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


async def update_user_reading_stats(telegram_user_id: int):
    """Обновление статистики чтения пользователя"""
    async with aiohttp.ClientSession() as session:
        url = f"{API_URL}/telegram-users/{telegram_user_id}/update_books_read/"
        try:
            async with session.post(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    logger.info(f"Статистика обновлена для пользователя {telegram_user_id}: {result}")
                    return result
                else:
                    error_text = await resp.text()
                    logger.warning(f"Не удалось обновить статистику: {resp.status} - {error_text}")
                    return None
        except Exception as e:
            logger.error(f"Ошибка при обновлении статистики: {e}")
            return None

async def add_xp_to_user(tg_id: int, xp_amount: int) -> dict:
    """
    Добавление XP пользователю.
    """
    async with aiohttp.ClientSession() as session:
        url = f"{API_URL}/telegram-users/{tg_id}/add_xp/"
        payload = {"xp_amount": xp_amount}

        try:
            async with session.post(url, json=payload) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    logger.info(f"Добавлено {xp_amount} XP пользователю {tg_id}")
                    return result
                else:
                    error_text = await resp.text()
                    logger.error(f"Ошибка при добавлении XP: {resp.status} - {error_text}")
                    return None
        except Exception as e:
            logger.error(f"Ошибка при добавлении XP пользователю {tg_id}: {e}")
            return None