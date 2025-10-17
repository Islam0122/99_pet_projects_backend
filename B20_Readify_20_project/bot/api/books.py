import aiohttp
import asyncio
import logging
from typing import Optional
from config.config import load_config

logger = logging.getLogger(__name__)
config = load_config()
API_URL = f"{config.api_url.api_url}"  # базовый URL API


async def fetch_books() -> list:
    """Получение списка всех книг"""
    url = f"{API_URL}/books/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.json()
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при получении списка книг: {e}")
            return []


async def fetch_chapter(book_id: int, chapter_number: int) -> dict:
    """Получение конкретной главы"""
    url = f"{API_URL}/books/{book_id}/chapters/{chapter_number}/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.json()
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при получении главы {chapter_number} книги {book_id}: {e}")
            return {}


async def load_book(olid: str) -> dict:
    """Авто-добавление книги через OLID"""
    url = f"{API_URL}/books/load/"
    payload = {"olid": olid}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload) as resp:
                resp.raise_for_status()
                return await resp.json()
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при загрузке книги OLID={olid}: {e}")
            return {}

