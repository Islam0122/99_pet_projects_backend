from dataclasses import dataclass
from typing import Optional
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class BaseApiUrl:
    api_url: str


@dataclass
class Config:
    bot: TgBot
    api_url: BaseApiUrl


def load_config(path: Optional[str] = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        bot=TgBot(
            token=env.str("TELEGRAM_BOT_TOKEN", default=""),
        ),
        api_url=BaseApiUrl(
            api_url=env.str("TELEGRAM_API_URL", default="https://api.telegram.org"),
        ),
    )
