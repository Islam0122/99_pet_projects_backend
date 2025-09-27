import aiohttp
import logging
from typing import Optional, Dict, Any, List
from config.config import load_config
from .redis_client import RedisClient

import json

logger = logging.getLogger(__name__)
config = load_config()
API_BASE = f"{config.api_url.api_url}"
DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=10)
REDIS_TTL = 120

class APIError(Exception):
    pass

class APIClient:
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None):
        self.base_url = (base_url or API_BASE).rstrip("/") + "/"
        self.token = token or ""
        self.session: Optional[aiohttp.ClientSession] = None
        self.redis_client = RedisClient(redis_url="redis://redis:6379/1")
        self._headers = {"Content-Type": "application/json"}
        if self.token:
            self._headers["Authorization"] = f"Token {self.token}"

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self._headers)
        await self.redis_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session and not self.session.closed:
            await self.session.close()
        await self.redis_client.__aexit__(exc_type, exc_val, exc_tb)

    async def _get(self, path: str, params: Optional[Dict[str, Any]] = None):
        url = self.base_url + path.lstrip("/")
        async with self.session.get(url, params=params) as resp:
            text = await resp.text()
            if resp.status >= 400:
                logger.error("GET %s -> %s: %s", url, resp.status, text)
                raise APIError(f"GET {url} returned {resp.status}")
            return await resp.json()

    async def get_categories(self) -> List[Dict[str, Any]]:
        cache_key = "categories"
        cached = await self.redis_client.get(cache_key)
        if cached:
            return cached

        res = await self._get("categories/")
        results = res.get("results", []) if isinstance(res, dict) else res
        await self.redis_client.set(cache_key, results)
        return results

    async def get_recipes_by_category(self, category_id: int, params: Optional[Dict[str, Any]] = None):
        cache_key = f"recipes_category:{category_id}"
        cached = await self.redis_client.get(cache_key)
        if cached:
            return cached

        if params is None:
            params = {}
        res = await self._get(f"recipes/?category={category_id}", params=params)
        await self.redis_client.set(cache_key, res)
        return res

    async def get_recipes(self, params: Optional[Dict[str, Any]] = None):
        return await self._get("recipes/", params=params)

    async def generate_recipe(self, prompt: str) -> str:
        res = await self._post("ai/generate-recipe/", json={"prompt": prompt})
        if isinstance(res, dict):
            return res.get("result") or res.get("ai_result") or str(res)
        return str(res)

    async def _post(self, path: str, json: Optional[Dict[str, Any]] = None):
        url = self.base_url + path.lstrip("/")
        async with self.session.post(url, json=json) as resp:
            text = await resp.text()
            if resp.status >= 400:
                logger.error("POST %s -> %s: %s", url, resp.status, text)
                raise APIError(f"POST {url} returned {resp.status}")
            if resp.content_type == "application/json":
                return await resp.json()
            return text

    async def get_popular_recipes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Если есть эндпоинт /recipes/popular/ или просто сортировка по посещениям/рейтингу."""
        # попытка вызвать popular endpoint
        try:
            res = await self._get("recipes/", params={"limit": limit})
            return res.get("results", []) if isinstance(res, dict) else res
        except APIError:
            # fallback: получить recipes?ordering=-views (или по created_at)
            res = await self.get_recipes(params={"ordering": "-created_at", "page_size": limit})
            return res.get("results", []) if isinstance(res, dict) else res


    async def get_user_recipes(
            self,
            telegram_id: int,
            params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Получить список рецептов пользователя.
        GET /user-recipes/?telegram_id=...
        """
        p = params.copy() if params else {}
        p.update({"telegram_id": telegram_id})

        res = await self._get("user-recipes/", params=p)

        # На случай, если API вернёт просто список
        if isinstance(res, dict):
            return res.get("results", [])
        return res if isinstance(res, list) else []

    async def create_user_recipe(
            self,
            user_id: int,
            category_id: Optional[int],
            user_text: str,
            ai_result: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Создать новый пользовательский рецепт.
        POST /user-recipes/
        """
        payload = {
            "user": user_id,
            "category": category_id,
            "user_text": user_text,
            "ai_result": ai_result,
        }

        res = await self._post("user-recipes/", json=payload)

        # Возвращаем dict (если сервер вдруг вернёт не то — подстрахуемся)
        return res if isinstance(res, dict) else {}


