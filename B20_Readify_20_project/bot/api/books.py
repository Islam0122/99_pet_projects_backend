import aiohttp
import logging
from config.config import load_config
from typing import Optional, Dict, List,BinaryIO
import aiohttp

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


async def fetch_user_books() -> List[Dict]:
    """📚 Получение списка всех пользовательских книг"""
    url = f"{API_URL}/user-books/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.json()
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при получении списка пользовательских книг: {e}")
            return []


async def create_user_book(
        title: str,
        description: str,
        telegram_user_id: int,
        file: BinaryIO,
        file_name: str
) -> bool:
    try:
        data = aiohttp.FormData()
        data.add_field('title', title)
        data.add_field('description', description)
        data.add_field('telegram_user', str(telegram_user_id))
        data.add_field('file', file, filename=file_name)

        async with aiohttp.ClientSession() as session:
            url = f"{API_URL}/user-books/"
            async with session.post(
                    url,
                    data=data
            ) as response:

                if response.status == 201:
                    return True
                else:
                    logger.error(f"API error: {response.status} - {await response.text()}")
                    return False

    except Exception as e:
        logger.error(f"Error creating user book: {e}")
        return False


async def delete_user_book(book_id: int) -> bool:
    """🗑️ Удаление пользовательской книги"""
    url = f"{API_URL}/user-books/{book_id}/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(url) as resp:
                if resp.status == 204:
                    logger.info(f"Книга с ID={book_id} успешно удалена.")
                    return True
                else:
                    logger.warning(f"Не удалось удалить книгу ID={book_id}. Код: {resp.status}")
                    return False
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при удалении книги ID={book_id}: {e}")
            return False


async def read_user_book(book_id: int) -> Optional[Dict]:
    """📖 Чтение файла книги с нумерацией строк"""
    url = f"{API_URL}/user-books/{book_id}/read_file/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.json()
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при чтении файла книги ID={book_id}: {e}")
            return None

