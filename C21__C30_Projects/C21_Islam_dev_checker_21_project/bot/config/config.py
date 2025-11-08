from dataclasses import dataclass
from typing import Optional
from environs import Env
from urllib.parse import urlparse


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
    password: Optional[str] = None
    username: Optional[str] = None


@dataclass
class Config:
    bot: TgBot
    api: ApiConfig
    redis: RedisConfig


def load_config(path: Optional[str] = None) -> Config:
    """
    Загружает конфигурацию из environment variables (включая REDIS_URL)
    """
    env = Env()
    env.read_env(path)

    # Если REDIS_URL есть, разбираем его
    redis_url = env.str("REDIS_URL", None)

    if redis_url:
        parsed = urlparse(redis_url)
        redis_host = parsed.hostname or "localhost"
        redis_port = parsed.port or 6379
        redis_db = int(parsed.path.strip("/")) if parsed.path else 0
        redis_password = parsed.password
        redis_username = parsed.username
    else:
        # Иначе берём из отдельных переменных
        redis_host = env.str("REDIS_HOST", "localhost")
        redis_port = env.int("REDIS_PORT", 6379)
        redis_db = env.int("REDIS_DB", 0)
        redis_password = None
        redis_username = None

    return Config(
        bot=TgBot(
            token=env.str("TELEGRAM_BOT_TOKEN"),
        ),
        api=ApiConfig(
            api_url=env.str("TELEGRAM_API_URL", "http://localhost:8000/api/v1")
        ),
        redis=RedisConfig(
            host=redis_host,
            port=redis_port,
            db=redis_db,
            password=redis_password,
            username=redis_username
        )
    )
