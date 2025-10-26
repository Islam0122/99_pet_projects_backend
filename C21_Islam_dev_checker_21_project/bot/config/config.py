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
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    url: Optional[str] = None  # если используется Railway REDIS_URL

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
        host=env.str("REDIS_HOST", "localhost"),
        port=env.int("REDIS_PORT", 6379),
        db=env.int("REDIS_DB", 0),
        password=env.str("REDIS_PASSWORD", None),
        url=env.str("REDIS_URL", None)  # Railway REDIS_URL
    )

    return Config(bot=bot, api=api, redis=redis_config)

# Пример подключения к Redis
def get_redis_connection(config: RedisConfig):
    if config.url:
        # Используем Railway REDIS_URL
        return redis.from_url(config.url, decode_responses=True)
    else:
        # Локальный Redis
        return redis.Redis(
            host=config.host,
            port=config.port,
            db=config.db,
            password=config.password,
            decode_responses=True
        )

# Использование
config = load_config()
r = get_redis_connection(config.redis)

print("Redis ping:", r.ping())
