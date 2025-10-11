import asyncio
import logging

from aiogram import Bot, Dispatcher,types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog.setup import DialogRegistry

from config.config import Config, load_config
from handlers.start import start_router
from handlers.profile import profile_router
from handlers.tasks import tasks_router
from dialogs.add_task_dialog import add_task_dialog
from dialogs.states import *
from aiogram_dialog import  setup_dialogs, DialogManager
from aiogram.filters import Command

logger = logging.getLogger(__name__)


async def main():
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
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)

    dp.workflow_data.update({
        "config": config,
    })
    setup_dialogs(dp)
    @dp.message(Command("add_task"))
    async def start_add_task(message: types.Message, dialog_manager: DialogManager):
        await dialog_manager.start(AddTaskSG.waiting_for_title)

    logger.info("🔗 Подключаем роутеры...")
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(tasks_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("❌ Bot stopped!")
