import aiohttp
import logging
from config.config import load_config
from typing import Optional, Dict, List,BinaryIO
import aiohttp

logger = logging.getLogger(__name__)
config = load_config()
API_URL = f"{config.api_url.api_url}"  # базовый URL API


async def fetch_books() -> List[Dict]:
    url = f"{API_URL}/books/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.json()
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при получении списка книг: {e}")
            return []


async def fetch_book_chapters(book_id: int) -> List[Dict]:
    url = f"{API_URL}/books/{book_id}/chapters/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.json()
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при получении глав книги {book_id}: {e}")
            return []


async def fetch_chapter(book_id: int, chapter_number: int) -> Optional[Dict]:
    url = f"{API_URL}/books/{book_id}/chapter/{chapter_number}/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return None
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при получении главы {chapter_number} книги {book_id}: {e}")
            return None


async def load_book_from_openlibrary(olid: str) -> Optional[Dict]:
    url = f"{API_URL}/load-book/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json={"olid": olid}) as resp:
                if resp.status == 201:
                    return await resp.json()
                else:
                    error_text = await resp.text()
                    logger.error(f"Ошибка при загрузке книги: {resp.status} - {error_text}")
                    return None
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при загрузке книги {olid}: {e}")
            return None


async def fetch_user_books() -> List[Dict]:
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


async def read_user_book(book_id: int, telegram_user_id: int = None) -> Optional[Dict]:
\    url = f"{API_URL}/user-books/{book_id}/read_file/"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    book_content = await resp.json()

                    if telegram_user_id:
                        from .telegramusers import update_user_reading_stats, add_xp_to_user
                        await update_user_reading_stats(telegram_user_id)
                        await add_xp_to_user(telegram_user_id, 10)  # +10 XP за чтение
                        logger.info(f"XP добавлен пользователю {telegram_user_id} за чтение книги {book_id}")

                    return book_content
                else:
                    error_text = await resp.text()
                    logger.error(f"Ошибка API при чтении книги {book_id}: {resp.status} - {error_text}")
                    return None
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при чтении файла книги ID={book_id}: {e}")
            return None