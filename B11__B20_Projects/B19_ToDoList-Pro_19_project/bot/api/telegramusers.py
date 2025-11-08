import aiohttp
import logging
from typing import Optional, List
from config.config import load_config
from datetime import datetime, timedelta

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
                return await resp.json()
            elif resp.status == 400:
                async with session.patch(url, json=payload) as resp2:
                    resp2.raise_for_status()
                    return await resp2.json()


async def delete_telegram_user(user_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{API_URL}/telegram-users/{user_id}/") as resp:
            resp.raise_for_status()
            return {"status": "deleted", "user_id": user_id}


async def mark_task_done_and_update_user(user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/telegram-users/{user_id}/") as resp:
            resp.raise_for_status()
            user_data = await resp.json()

    today = datetime.utcnow().date()
    last_completed = user_data.get("last_task_completed")
    if last_completed:
        last_date = datetime.fromisoformat(last_completed).date()
        if last_date == today - timedelta(days=1):
            streak = user_data.get("streak_days", 0) + 1
        elif last_date < today - timedelta(days=1):
            streak = 1
        else:
            streak = user_data.get("streak_days", 0)  # уже сделал сегодня
    else:
        streak = 1

    total_completes = user_data.get("total_task_completes", 0) + 1

    async with aiohttp.ClientSession() as session:
        async with session.patch(
            f"{API_URL}/telegram-users/{user_id}/",
            json={
                "total_task_completes": total_completes,
                "streak_days": streak,
                "last_task_completed": today.isoformat()
            }
        ) as resp:
            resp.raise_for_status()
            return await resp.json()

