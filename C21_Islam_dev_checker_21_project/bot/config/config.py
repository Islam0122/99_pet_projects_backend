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
    url: Optional[str] = None

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
        url=env.str("REDIS_URL", None)  # Railway REDIS_URL
    )

    return Config(bot=bot, api=api, redis=redis_config)

