from unicodedata import category

import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any, List
from config.config import load_config

logger = logging.getLogger(__name__)
config = load_config()
API_BASE = f"{config.api_url.api_url}"
HEADERS = {"Content-Type": "application/json"}

DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=10)


class APIError(Exception):
    pass


class APIClient:
    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None, timeout: Optional[aiohttp.ClientTimeout] = None):
        self.base_url = (base_url or API_BASE).rstrip("/") + "/"
        self.token = token or ""
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.session: Optional[aiohttp.ClientSession] = None
        self._headers = {"Content-Type": "application/json"}

        # если у тебя есть авторизация (Token / Bearer)
        if self.token:
            # Пример: Token <token> или Bearer <token>
            self._headers["Authorization"] = f"Token {self.token}"

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout, headers=self._headers)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session and not self.session.closed:
            await self.session.close()

    # ---- Utility ----
    async def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = self.base_url + path.lstrip("/")
        try:
            async with self.session.get(url, params=params) as resp:
                text = await resp.text()
                if resp.status >= 400:
                    logger.error("GET %s -> %s: %s", url, resp.status, text)
                    raise APIError(f"GET {url} returned {resp.status}")
                return await resp.json()
        except aiohttp.ClientError as e:
            logger.exception("Network error GET %s", url)
            raise APIError(str(e))

    async def _post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        url = self.base_url + path.lstrip("/")
        try:
            async with self.session.post(url, json=json) as resp:
                text = await resp.text()
                if resp.status >= 400:
                    logger.error("POST %s -> %s: %s", url, resp.status, text)
                    raise APIError(f"POST {url} returned {resp.status}")
                # some endpoints might return no content
                if resp.content_type == "application/json":
                    return await resp.json()
                return text
        except aiohttp.ClientError as e:
            logger.exception("Network error POST %s", url)
            raise APIError(str(e))

    async def _patch(self, path: str, json: Optional[Dict[str, Any]] = None) -> Any:
        url = self.base_url + path.lstrip("/")
        try:
            async with self.session.patch(url, json=json) as resp:
                text = await resp.text()
                if resp.status >= 400:
                    logger.error("PATCH %s -> %s: %s", url, resp.status, text)
                    raise APIError(f"PATCH {url} returned {resp.status}")
                return await resp.json()
        except aiohttp.ClientError as e:
            logger.exception("Network error PATCH %s", url)
            raise APIError(str(e))

    async def _delete(self, path: str) -> int:
        url = self.base_url + path.lstrip("/")
        try:
            async with self.session.delete(url) as resp:
                return resp.status
        except aiohttp.ClientError as e:
            logger.exception("Network error DELETE %s", url)
            raise APIError(str(e))


    # ---- Category / Recipe endpoints ----
    async def get_categories(self) -> List[Dict[str, Any]]:
        res = await self._get("categories/")
        return res.get("results", []) if isinstance(res, dict) else res

    async def get_recipes(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """GET /recipes/ with optional params (search, ordering, category, page)"""
        return await self._get("recipes/", params=params)

    async def get_recipes_by_category(
            self,
            category_id: int,
            params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """GET /recipes/ filtered by category (with optional params like search, ordering, page)"""

        if params is None:
            params = {}

        return await self._get(f"recipes/?category={category_id}", params=params)

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


    # ---- UserRecipe endpoints ----
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

    # ---- Custom: call AI generation endpoint (если есть) ----
    async def generate_recipe(self, prompt: str) -> str:
        """
        Если у тебя есть endpoint /generate-recipe/ или /ai/generate/, вызови его.
        Иначе вместо этого можно вызвать внешнюю функцию для GigaChat/GPT.
        """
        try:
            res = await self._post("ai/generate-recipe/", json={"prompt": prompt})
            # ожидаем {'result': '...'} или raw text
            if isinstance(res, dict):
                return res.get("result") or res.get("ai_result") or str(res)
            return str(res)
        except APIError:
            # fallback — вернуть понятную ошибку для UI
            logger.exception("AI generation failed")
            raise
