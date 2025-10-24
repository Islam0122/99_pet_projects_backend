from dataclasses import dataclass
from typing import Optional
from environs import Env
import os


@dataclass
class TgBot:
    token: str


@dataclass
class ApiConfig:
    api_url: str


@dataclass
class RedisConfig:
    host: str
    port: int
    db: int


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

    return Config(
        bot=TgBot(
            token=env.str("TELEGRAM_BOT_TOKEN"),
        ),
        api=ApiConfig(
            api_url=env.str("TELEGRAM_API_URL", "http://localhost:8000/api/vq")
        ),
        redis=RedisConfig(
            host=env.str("REDIS_HOST", "localhost"),
            port=env.int("REDIS_PORT", 6379),
            db=env.int("REDIS_DB", 1)
        )
    )