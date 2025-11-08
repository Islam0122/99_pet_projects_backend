import aiohttp
import logging
from typing import Optional, List
from config.config import load_config

logger = logging.getLogger(__name__)
config = load_config()
API_URL = f"{config.api_url.api_url}"


async def get_categories() -> List[dict]:
    """Получение всех категорий"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/categories/") as resp:
            resp.raise_for_status()
            return await resp.json()


async def get_tasks() -> List[dict]:
    """Получение всех задач"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/tasks/") as resp:
            resp.raise_for_status()
            return await resp.json()

async def get_tasks_by_telegram_id(tg_id: int):
    async with aiohttp.ClientSession() as session:
        url = f"{API_URL}/tasks/?telegram_id={tg_id}"
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.json()

async def get_task_by_id(task_id: int) -> dict:
    """Получение одной задачи по ID"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/tasks/{task_id}/") as resp:
            resp.raise_for_status()
            return await resp.json()


async def create_task(
    owner: int,
    title: str,
    description: Optional[str] = None,
    category_ids: Optional[List[int]] = None,
    due_date: Optional[str] = None,
    done: bool = False
) -> dict:
    payload = {
        "owner": owner,
        "title": title,
        "description": description or "",
        "done": done,
        "category_ids": category_ids or [],
        "due_date": due_date
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/tasks/", json=payload) as resp:
            resp.raise_for_status()
            return await resp.json()


async def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    done: Optional[bool] = None,
    category_ids: Optional[List[int]] = None,
    due_date: Optional[str] = None
) -> dict:
    payload = {}
    if title is not None:
        payload["title"] = title
    if description is not None:
        payload["description"] = description
    if done is not None:
        payload["done"] = done
    if category_ids is not None:
        payload["category_ids"] = category_ids
    if due_date is not None:
        payload["due_date"] = due_date

    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{API_URL}/tasks/{task_id}/", json=payload) as resp:
            resp.raise_for_status()
            return await resp.json()


async def delete_task(task_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{API_URL}/tasks/{task_id}/") as resp:
            resp.raise_for_status()
            return {"status": "deleted", "task_id": task_id}

async def mark_task_done(task_id: int):
    """Отметить задачу как выполненную"""
    async with aiohttp.ClientSession() as session:
        url = f"{API_URL}/tasks/{task_id}/"
        payload = {"done": True}
        async with session.patch(url, json=payload) as resp:
            resp.raise_for_status()
            return await resp.json()

