import aiohttp
from config.config import load_config
import redis.asyncio as redis
import json
import logging
import aiohttp
from pathlib import Path
from typing import Optional, Dict, Any, List
import os
import asyncio
from typing import Optional

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
            # Используем redis_url из конфига
            self.redis = redis.Redis.from_url(
                config.redis.url,
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

                # Успешные статусы
                if response.status in [200, 201]:
                    # Для DELETE запросов может не быть тела
                    if method.upper() == 'DELETE' and response.status == 204:
                        return {"success": True}

                    try:
                        content_type = response.headers.get('Content-Type', '')
                        if 'application/json' in content_type:
                            return await response.json()
                        else:
                            text_response = await response.text()
                            logging.info(f"Non-JSON response for {url}: {text_response}")
                            return {"success": True, "text": text_response}
                    except Exception as e:
                        logging.warning(f"JSON parse error for {url}: {e}")
                        return {"success": True}

                # Ошибки клиента
                elif response.status in [400, 401, 403, 404]:
                    error_text = await response.text()
                    logging.warning(f"Client error {response.status} for {url}: {error_text}")
                    if response.status == 404:
                        logging.info(f"Resource not found: {url}")
                        return None
                    try:
                        error_data = json.loads(error_text)
                        return {"error": error_data}
                    except:
                        return {"error": error_text}

                # Серверные ошибки
                else:
                    error_text = await response.text()
                    logging.error(f"HTTP error {response.status} for {url}: {error_text}")
                    return {"error": f"Server error: {response.status}"}

        except aiohttp.ClientError as e:
            logging.error(f"Network error for {url}: {e}")
            return {"error": f"Network error: {str(e)}"}
        except Exception as e:
            logging.error(f"Unexpected error for {url}: {e}")
            return {"error": f"Unexpected error: {str(e)}"}


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


class HWMonth3(BaseAPI):

    BASE_URL = f"{config.api.api_url}/month3/"

    def __init__(self):
        super().__init__(self.BASE_URL)

    async def create_homework(
            self,
            student_id: int,
            lesson: str,
            title: str,
            task_condition: str,
            github_url: str = None
    ) -> Optional[Dict]:
        """Создать домашку"""
        payload = {
            "student": student_id,
            "lesson": lesson,
            "title": title,
            "task_condition": task_condition,
            "github_url": github_url
        }

        result = await self._make_request("POST", self.base_url, json=payload)

        # Проверяем результат
        if result and "error" not in result:
            # Инвалидируем кэш связанный со студентом
            return result
        else:
            # Логируем ошибку и возвращаем None
            error_msg = result.get("error", "Unknown error") if result else "No response"
            logging.error(f"Failed to create homework: {error_msg}")
            return None

    async def get_homeworks(
            self,
            student_id: int = None,
            lesson: str = None,
            is_checked: bool = None,
            use_cache: bool = True
    ) -> List[Dict]:
        """Получить домашки с фильтрацией"""
        cache_key_parts = ["month3"]
        if student_id:
            cache_key_parts.append(f"student:{student_id}")
        if lesson:
            cache_key_parts.append(f"lesson:{lesson}")
        if is_checked is not None:
            cache_key_parts.append(f"checked:{is_checked}")

        cache_key = ":".join(cache_key_parts)

        if use_cache:
            cached = await self._get_cached_data(cache_key)
            if cached:
                return cached

        params = {}
        if student_id:
            params["student"] = student_id
        if lesson:
            params["lesson"] = lesson
        if is_checked is not None:
            params["is_checked"] = str(is_checked).lower()

        result = await self._make_request("GET", self.base_url, params=params)

        # Обрабатываем результат
        if result and "error" not in result:
            if use_cache:
                await self._set_cached_data(cache_key, result)
            return result
        else:
            logging.error(
                f"Failed to get homeworks: {result.get('error', 'Unknown error') if result else 'No response'}")
            return []

    async def get_homework_by_id(self, homework_id: int, use_cache: bool = True) -> Optional[Dict]:
        """Получить конкретную домашку по ID"""
        cache_key = f"month3:id:{homework_id}"

        if use_cache:
            cached = await self._get_cached_data(cache_key)
            if cached:
                return cached

        url = f"{self.base_url}{homework_id}/"
        result = await self._make_request("GET", url)

        if result and "error" not in result:
            if use_cache:
                await self._set_cached_data(cache_key, result)
            return result
        else:
            return None


class HWMonth2(BaseAPI):
    BASE_URL = f"{config.api.api_url}/month2/"

    def __init__(self):
        super().__init__(self.BASE_URL)

    async def create_homework(
            self,
            student_id: int,
            lesson: str,
            title: str,
            task_condition: str,
            github_url: str = None
    ) -> Optional[Dict]:
        """Создать домашку"""
        payload = {
            "student": student_id,
            "lesson": lesson,
            "title": title,
            "task_condition": task_condition,
            "github_url": github_url
        }

        result = await self._make_request("POST", self.base_url, json=payload)

        # Проверяем результат
        if result and "error" not in result:
            # Инвалидируем кэш связанный со студентом
            return result
        else:
            # Логируем ошибку и возвращаем None
            error_msg = result.get("error", "Unknown error") if result else "No response"
            logging.error(f"Failed to create homework: {error_msg}")
            return None

    async def get_homeworks(
            self,
            student_id: int = None,
            lesson: str = None,
            is_checked: bool = None,
            use_cache: bool = True
    ) -> List[Dict]:
        """Получить домашки с фильтрацией"""
        cache_key_parts = ["month2"]
        if student_id:
            cache_key_parts.append(f"student:{student_id}")
        if lesson:
            cache_key_parts.append(f"lesson:{lesson}")
        if is_checked is not None:
            cache_key_parts.append(f"checked:{is_checked}")

        cache_key = ":".join(cache_key_parts)

        if use_cache:
            cached = await self._get_cached_data(cache_key)
            if cached:
                return cached

        params = {}
        if student_id:
            params["student"] = student_id
        if lesson:
            params["lesson"] = lesson
        if is_checked is not None:
            params["is_checked"] = str(is_checked).lower()

        result = await self._make_request("GET", self.base_url, params=params)

        # Обрабатываем результат
        if result and "error" not in result:
            if use_cache:
                await self._set_cached_data(cache_key, result)
            return result
        else:
            logging.error(
                f"Failed to get homeworks: {result.get('error', 'Unknown error') if result else 'No response'}")
            return []

    async def get_homework_by_id(self, homework_id: int, use_cache: bool = True) -> Optional[Dict]:
        """Получить конкретную домашку по ID"""
        cache_key = f"month2:id:{homework_id}"

        if use_cache:
            cached = await self._get_cached_data(cache_key)
            if cached:
                return cached

        url = f"{self.base_url}{homework_id}/"
        result = await self._make_request("GET", url)

        if result and "error" not in result:
            if use_cache:
                await self._set_cached_data(cache_key, result)
            return result
        else:
            return None


class HWMonth1(BaseAPI):
    BASE_URL = f"{config.api.api_url}/month1/"

    def __init__(self):
        super().__init__(self.BASE_URL)

    async def get_homeworks(
            self,
            student_id: int = None,
            lesson: str = None,
            is_checked: bool = None,
            use_cache: bool = True
    ) -> List[Dict]:
        """Получить домашки с фильтрацией"""
        cache_key_parts = ["month1"]
        if student_id:
            cache_key_parts.append(f"student:{student_id}")
        if lesson:
            cache_key_parts.append(f"lesson:{lesson}")
        if is_checked is not None:
            cache_key_parts.append(f"checked:{is_checked}")

        cache_key = ":".join(cache_key_parts)

        if use_cache:
            cached = await self._get_cached_data(cache_key)
            if cached:
                return cached

        params = {}
        if student_id:
            params["student"] = student_id
        if lesson:
            params["lesson"] = lesson
        if is_checked is not None:
            params["is_checked"] = str(is_checked).lower()

        result = await self._make_request("GET", self.base_url, params=params)

        if result and "error" not in result:
            if use_cache:
                await self._set_cached_data(cache_key, result)
            return result
        else:
            logging.error(
                f"Failed to get homeworks: {result.get('error', 'Unknown error') if result else 'No response'}")
            return []

    async def get_homework_by_id(self, homework_id: int, use_cache: bool = True) -> Optional[Dict]:
        """Получить конкретную домашку по ID"""
        cache_key = f"month1:id:{homework_id}"

        if use_cache:
            cached = await self._get_cached_data(cache_key)
            if cached:
                return cached

        url = f"{self.base_url}{homework_id}/"
        result = await self._make_request("GET", url)

        if result and "error" not in result:
            if use_cache:
                await self._set_cached_data(cache_key, result)
            return result
        else:
            return None

    async def create_homework(
            self,
            student_id: int,
            lesson: str,
            tasks: List[Dict]
    ) -> Optional[Dict]:
        """Создать домашнее задание для 1-го месяца"""
        payload = {
            "student": student_id,
            "lesson": lesson,
            "tasks": tasks
        }

        result = await self._make_request("POST", self.base_url, json=payload)

        if result and "error" not in result:
            # Инвалидируем кэш связанный со студентом
            cache_keys_to_delete = [
                f"month1:student:{student_id}",
                f"month1:student:{student_id}:checked:false",
                "month1:all"
            ]
            for key in cache_keys_to_delete:
                await self.redis.delete(key)
            return result
        else:
            error_msg = result.get("error", "Unknown error") if result else "No response"
            logging.error(f"Failed to create homework: {error_msg}")
            return None

    async def recheck_homework(self, homework_id: int) -> Optional[Dict]:
        """Запросить перепроверку домашнего задания"""
        url = f"{self.base_url}{homework_id}/recheck/"
        result = await self._make_request("POST", url)

        if result and "error" not in result:
            # Инвалидируем кэш для этого homework
            await self.redis.delete(f"month1:id:{homework_id}")
            return result
        else:
            error_msg = result.get("error", "Unknown error") if result else "No response"
            logging.error(f"Failed to recheck homework: {error_msg}")
            return None

    async def get_student_homeworks(self, student_id: int, use_cache: bool = True) -> List[Dict]:
        """Получить все домашние работы конкретного студента"""
        return await self.get_homeworks(student_id=student_id, use_cache=use_cache)

    async def get_checked_tasks(self, student_id: int, use_cache: bool = True) -> List[Dict]:
        """Получить проверенные задания студента"""
        homeworks = await self.get_homeworks(student_id=student_id, use_cache=use_cache)
        checked_tasks = []

        for homework in homeworks:
            checked_items = [item for item in homework.get('items', []) if item.get('is_checked')]
            if checked_items:
                homework_copy = homework.copy()
                homework_copy['items'] = checked_items
                checked_tasks.append(homework_copy)

        return checked_tasks

    async def get_pending_tasks(self, student_id: int, use_cache: bool = True) -> List[Dict]:
        """Получить задания, ожидающие проверки"""
        homeworks = await self.get_homeworks(student_id=student_id, use_cache=use_cache)
        pending_tasks = []

        for homework in homeworks:
            pending_items = [item for item in homework.get('items', []) if not item.get('is_checked')]
            if pending_items:
                homework_copy = homework.copy()
                homework_copy['items'] = pending_items
                pending_tasks.append(homework_copy)

        return pending_tasks

    async def get_available_lessons(self, use_cache: bool = True) -> List[Dict]:
        """Получить список доступных уроков"""
        cache_key = "month1:lessons"

        if use_cache:
            cached = await self._get_cached_data(cache_key)
            if cached:
                return cached

        url = f"{self.base_url}lessons/"
        result = await self._make_request("GET", url)

        if result and "error" not in result:
            if use_cache:
                await self._set_cached_data(cache_key, result, ttl=3600)  # Долгий TTL для уроков
            return result
        else:
            logging.error(f"Failed to get lessons: {result.get('error', 'Unknown error') if result else 'No response'}")
            return []

    async def update_grade(
            self,
            homework_id: int,
            item_id: int,
            grade: float
    ) -> Optional[Dict]:
        """Обновить оценку задания вручную"""
        url = f"{self.base_url}{homework_id}/update-grade/"
        payload = {
            "item_id": item_id,
            "grade": max(0, min(10, grade))  # Ограничение 0-10
        }

        result = await self._make_request("PATCH", url, json=payload)

        if result and "error" not in result:
            # Инвалидируем кэш
            await self.redis.delete(f"month1:id:{homework_id}")
            return result
        else:
            error_msg = result.get("error", "Unknown error") if result else "No response"
            logging.error(f"Failed to update grade: {error_msg}")
            return None

    async def get_student_stats(self, student_id: int, use_cache: bool = True) -> Dict[str, Any]:
        """Получить статистику студента по 1-му месяцу"""
        cache_key = f"month1:student:{student_id}:stats"

        if use_cache:
            cached = await self._get_cached_data(cache_key)
            if cached:
                return cached

        homeworks = await self.get_student_homeworks(student_id, use_cache=False)

        stats = {
            "total_homeworks": len(homeworks),
            "total_tasks": 0,
            "checked_tasks": 0,
            "pending_tasks": 0,
            "average_grade": 0,
            "completed_lessons": [],
            "pending_lessons": []
        }

        all_grades = []

        for homework in homeworks:
            lesson = homework.get('lesson')
            items = homework.get('items', [])
            stats["total_tasks"] += len(items)

            checked_count = sum(1 for item in items if item.get('is_checked'))
            stats["checked_tasks"] += checked_count
            stats["pending_tasks"] += len(items) - checked_count

            # Собираем оценки
            for item in items:
                if item.get('is_checked') and item.get('grade') is not None:
                    all_grades.append(item['grade'])

            # Определяем статус урока
            if all(item.get('is_checked') for item in items):
                stats["completed_lessons"].append(lesson)
            else:
                stats["pending_lessons"].append(lesson)

        # Рассчитываем среднюю оценку
        if all_grades:
            stats["average_grade"] = sum(all_grades) / len(all_grades)

        if use_cache:
            await self._set_cached_data(cache_key, stats)

        return stats