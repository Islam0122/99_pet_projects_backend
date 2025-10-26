from dataclasses import dataclass
from typing import Optional
from environs import Env
import os
import redis

@dataclass
class TgBot:
    token: str

@dataclass
class ApiConfig:
    api_url: str

@dataclass
class RedisConfig:
    url: Optional[str] = None      # Для Railway REDIS_URL
    host: Optional[str] = None     # Локальный Redis
    port: Optional[int] = None
    db: Optional[int] = None
    password: Optional[str] = None

@dataclass
class Config:
    bot: TgBot
    api: ApiConfig
    redis: RedisConfig

def load_config(path: Optional[str] = None) -> Config:
    """
    Загружает конфигурацию из environment variables
    """
    env = Env()
    env.read_env(path)

    # Telegram
    bot = TgBot(
        token=env.str("TELEGRAM_BOT_TOKEN")
    )

    # API
    api = ApiConfig(
        api_url=env.str("TELEGRAM_API_URL", "http://localhost:8000/api/v1")
    )

    # Redis
    redis_config = RedisConfig(
        url=env.str("REDIS_URL", None),            # Railway
        host=env.str("REDIS_HOST", "localhost"),   # Локально
        port=env.int("REDIS_PORT", 6379),
        db=env.int("REDIS_DB", 0),
        password=env.str("REDIS_PASSWORD", None)
    )

    return Config(bot=bot, api=api, redis=redis_config)
