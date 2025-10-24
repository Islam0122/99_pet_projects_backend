import aiohttp
from config.config import load_config
import redis.asyncio as redis
import json
import logging

# Загружаем конфиг один раз
config = load_config()

BASE_URL_STUDENTS = f"{config.api.api_url}/students/"
BASE_URL_GROUPS = f"{config.api.api_url}/groups/"
HEADERS = {"Content-Type": "application/json"}
REDIS_TTL = 120


class BaseAPI:
    """Базовый класс для API клиентов"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = HEADERS
        self.session = None
        self.redis = None
        self.redis_connected = False

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        try:
            self.redis = redis.Redis(
                host=config.redis.host,
                port=config.redis.port,
                db=config.redis.db,
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2
            )
            await self.redis.ping()
            self.redis_connected = True
            logging.info("Redis connected successfully")
        except Exception as e:
            logging.warning(f"Redis connection failed: {e}")
            self.redis_connected = False
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        if self.redis_connected:
            await self.redis.close()

    async def _get_cached_data(self, key: str):
        """Получить данные из кэша Redis"""
        if not self.redis_connected:
            return None
        try:
            cached = await self.redis.get(key)
            if cached:
                return json.loads(cached)
        except Exception as e:
            logging.warning(f"Redis cache error (get): {e}")
        return None

    async def _set_cached_data(self, key: str, data, ttl: int = REDIS_TTL):
        """Сохранить данные в кэш Redis"""
        if not self.redis_connected:
            return
        try:
            await self.redis.setex(key, ttl, json.dumps(data, default=str))
        except Exception as e:
            logging.warning(f"Redis cache error (set): {e}")

    async def _make_request(self, method: str, url: str, **kwargs):
        """Универсальный метод для выполнения запросов"""
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with self.session.request(
                    method, url, headers=self.headers, timeout=timeout, **kwargs
            ) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    logging.info(f"Resource not found: {url}")
                    return None
                else:
                    error_text = await response.text()
                    logging.error(f"HTTP error {response.status}: {error_text}")
                    return None
        except aiohttp.ClientError as e:
            logging.error(f"Network error for {url}: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error for {url}: {e}")
            return None


class StudentAPI(BaseAPI):
    """API для работы со студентами"""

    def __init__(self):
        super().__init__(BASE_URL_STUDENTS)

    async def get_student_by_telegram_id(self, telegram_id: str, use_cache: bool = True):
        """Получить студента по Telegram ID"""
        cache_key = f"student:{telegram_id}"

        if use_cache and self.redis_connected:
            cached_data = await self._get_cached_data(cache_key)
            if cached_data:
                return cached_data

        url = f"{self.base_url}{telegram_id}/"
        data = await self._make_request("GET", url)

        if data and self.redis_connected:
            await self._set_cached_data(cache_key, data)

        return data

    async def create_student(self, student_data: dict):
        """Создать нового студента"""
        data = await self._make_request("POST", self.base_url, json=student_data)
        if data and self.redis_connected:
            await self.redis.delete("students:all")
        return data

    async def update_student(self, telegram_id: str, update_data: dict):
        """Обновить данные студента"""
        url = f"{self.base_url}{telegram_id}/"
        data = await self._make_request("PATCH", url, json=update_data)
        if data and self.redis_connected:
            await self.redis.delete("students:all")
            await self.redis.delete(f"student:{telegram_id}")
        return data

    async def get_student_progress(self, telegram_id: str):
        """Получить прогресс студента"""
        url = f"{self.base_url}{telegram_id}/progress/"
        return await self._make_request("GET", url)

    async def get_active_students(self):
        """Получить активных студентов"""
        url = f"{self.base_url}active/"
        return await self._make_request("GET", url)

    async def get_top_students(self, limit: int = 5):
        """Получить топ студентов"""
        url = f"{self.base_url}top/?limit={limit}"
        return await self._make_request("GET", url)




class GroupsAPI(BaseAPI):
    """API для работы с группами"""

    def __init__(self):
        super().__init__(BASE_URL_GROUPS)

    async def get_all_groups(self, use_cache: bool = True):
        """Получить все группы"""
        cache_key = "groups:all"

        if use_cache and self.redis_connected:
            cached_data = await self._get_cached_data(cache_key)
            if cached_data:
                return cached_data

        data = await self._make_request("GET", self.base_url)

        if data and self.redis_connected:
            await self._set_cached_data(cache_key, data)

        return data

    async def get_group_by_telegram_id(self, telegram_id: str, use_cache: bool = True):
        """Получить группу по Telegram ID"""
        cache_key = f"group:{telegram_id}"

        if use_cache and self.redis_connected:
            cached_data = await self._get_cached_data(cache_key)
            if cached_data:
                return cached_data

        url = f"{self.base_url}{telegram_id}/"
        data = await self._make_request("GET", url)

        if data and self.redis_connected:
            await self._set_cached_data(cache_key, data)

        return data

    async def get_group_students(self, group_telegram_id: str, use_cache: bool = True):
        """Получить студентов группы"""
        cache_key = f"group:{group_telegram_id}:students"

        if use_cache and self.redis_connected:
            cached_data = await self._get_cached_data(cache_key)
            if cached_data:
                return cached_data

        url = f"{self.base_url}{group_telegram_id}/students/"
        data = await self._make_request("GET", url)

        if data and self.redis_connected:
            await self._set_cached_data(cache_key, data)

        return data

    async def create_group(self, group_data: dict):
        """Создать новую группу"""
        data = await self._make_request("POST", self.base_url, json=group_data)
        if data and self.redis_connected:
            await self.redis.delete("groups:all")
        return data