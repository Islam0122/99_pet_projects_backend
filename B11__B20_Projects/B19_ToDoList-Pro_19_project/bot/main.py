import asyncio
import logging
from aiogram import Bot, Dispatcher,types,F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config.config import Config, load_config
from handlers.start import start_router
from handlers.profile import profile_router
from handlers.tasks import tasks_router
from aiogram_dialog import  setup_dialogs, DialogManager
from aiogram.filters import Command
from dialogs.add_task_dialog import  AddTaskSG,create_add_task_dialog

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
    add_task_dialog = await create_add_task_dialog()
    @dp.message(F.text == "/add")
    async def start_add_task(message: types.Message, dialog_manager):
        await dialog_manager.start(AddTaskSG.waiting_for_title,)

    logger.info("🔗 Подключаем роутеры...")
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(tasks_router)
    dp.include_router(add_task_dialog)
    setup_dialogs(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("❌ Bot stopped!")
