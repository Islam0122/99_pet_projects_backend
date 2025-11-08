import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage  # простое хранилище для FSM

from config.config import Config, load_config
from keyboards.main_menu import set_main_menu
from handlers.user import user_router
from handlers.generate import generate_router
# Логгер
logger = logging.getLogger(__name__)


async def main():
    # Настраиваем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s"
    )
    logger.info("🚀 Starting bot...")

    # Загружаем конфиг
    config: Config = load_config()

    # Хранилище (можно заменить на RedisStorage или другое)
    storage = MemoryStorage()

    # Бот и диспетчер
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    # Тут можно инициализировать другие сервисы (БД, Redis и т.д.)
    dp.workflow_data.update({
        "config": config,
    })

    # Настраиваем меню
    await set_main_menu(bot,language="ru")

    # Подключаем роутеры
    logger.info("🔗 Подключаем роутеры...")
    dp.include_router(user_router)
    dp.include_router(generate_router)

    # Подключаем middlewares (если есть)
    logger.info("⚡ Подключаем миддлвари...")

    # Убираем вебхуки, если были, и стартуем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("❌ Bot stopped!")
