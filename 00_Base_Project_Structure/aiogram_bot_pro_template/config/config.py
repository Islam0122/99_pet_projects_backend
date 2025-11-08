from aiogram.enums import ParseMode
from dynaconf import Dynaconf
from pydantic import BaseModel, Field


class LogsConfig(BaseModel):
    level_name: str = Field(
        default="INFO", description="Log level name (e.g. DEBUG, INFO, WARNING, ERROR)."
    )
    format: str = Field(
        default="%(asctime)s [%(levelname)s] %(message)s",
        description="Log message format."
    )


class I18nConfig(BaseModel):
    default_locale: str = Field(default="en", description="Default locale for the application.")
    locales: list[str] = Field(default=["en"], description="List of supported locales.")


class BotConfig(BaseModel):
    token: str = Field(..., description="Telegram bot API token.")
    parse_mode: ParseMode = Field(
        ..., description="Default parse mode for sending messages (e.g. HTML, Markdown)."
    )


class PostgresConfig(BaseModel):
    name: str = Field(..., description="PostgreSQL database name.")
    host: str = Field(..., description="PostgreSQL server hostname.")
    port: int = Field(..., description="PostgreSQL server port.")
    user: str = Field(..., description="PostgreSQL username.")
    password: str = Field(..., description="PostgreSQL user password.")


class RedisConfig(BaseModel):
    host: str = Field(default="localhost", description="Redis server hostname.")
    port: int = Field(default=6379, description="Redis server port.")
    database: int = Field(default=0, description="Redis database index.")
    username: str | None = Field(None, description="Optional Redis username.")
    password: str | None = Field(None, description="Optional Redis password.")


class NatsConfig(BaseModel):
    servers: str | list[str] = Field(..., description="NATS servers.")
    delayed_consumer_subject: str = Field(..., description="NATS subject for delayed consumer.")
    delayed_consumer_stream: str = Field(..., description="NATS stream for delayed messages.")
    delayed_consumer_durable_name: str = Field(
        ..., description="Durable consumer name for delayed processing."
    )


class CacheConfig(BaseModel):
    use_cache: bool = Field(..., description="Enable or disable in-memory cache usage.")


class AppConfig(BaseModel):
    logs: LogsConfig
    i18n: I18nConfig
    bot: BotConfig
    postgres: PostgresConfig
    redis: RedisConfig
    nats: NatsConfig
    cache: CacheConfig


# Инициализация Dynaconf
_settings = Dynaconf(
    envvar_prefix=False,  # "DYNACONF",
    environments=True,  # Автоматически использовать секцию текущей среды
    env_switcher="ENV_FOR_DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
    load_dotenv=True,
)


def get_config() -> AppConfig:
    """
        Returns a typed application configuration.

        Returns:
            AppConfig: A validated Pydantic model containing the application settings.
    """
    logs = LogsConfig(
        level_name=_settings.logs.level_name,
        format=_settings.logs.format,
    )

    i18n = I18nConfig(
        default_locale=_settings.i18n.default_locale,
        locales=_settings.i18n.locales,
    )

    bot = BotConfig(
        token=_settings.bot_token,
        parse_mode=_settings.bot.parse_mode,
    )

    postgres = PostgresConfig(
        name=_settings.postgres.name,
        host=_settings.postgres.host,
        port=_settings.postgres.port,
        user=_settings.postgres.user,
        password=_settings.postgres_password,
    )

    redis = RedisConfig(
        host=_settings.redis.host,
        port=_settings.redis.port,
        database=_settings.redis.database,
        username=_settings.redis_username,
        password=_settings.redis_password,
    )

    nats = NatsConfig(
        servers=_settings.nats.servers,
        delayed_consumer_subject=_settings.nats.delayed_consumer_subject,
        delayed_consumer_stream=_settings.nats.delayed_consumer_stream,
        delayed_consumer_durable_name=_settings.nats.delayed_consumer_durable_name,
    )

    cache = CacheConfig(use_cache=_settings.cache.use_cache)

    return AppConfig(
        logs=logs,
        i18n=i18n,
        bot=bot,
        postgres=postgres,
        redis=redis,
        nats=nats,
        cache=cache,
    )
