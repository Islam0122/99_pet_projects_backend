import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage  # простое хранилище для FSM

from config.config import Config, load_config
from keyboards.main_menu import set_main_menu
from handlers.start import start_router
from handlers.profile import profile_router
from handlers.month3 import month3_router
from handlers.month2 import month2_router
from handlers.month1 import month1_router


logger = logging.getLogger(__name__)


async def main():
    # Настраиваем логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s"
    )
    logger.info("🚀 Starting bot...")
    config: Config = load_config()
    storage = MemoryStorage()
    bot = Bot(
        token=config.bot.token,
    )
    dp = Dispatcher(storage=storage)

    dp.workflow_data.update({
        "config": config,
    })

    await set_main_menu(bot)

    logger.info("🔗 Подключаем роутеры...")
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(month2_router)
    dp.include_router(month3_router)
    dp.include_router(month1_router)

    logger.info("⚡ Подключаем миддлвари...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("❌ Bot stopped!")
