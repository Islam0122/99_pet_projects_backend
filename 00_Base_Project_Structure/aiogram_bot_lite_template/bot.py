from aiogram import Bot, Dispatcher
from handlers import start, echo
import config
import asyncio

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    # Регистрируем хендлеры
    dp.include_router(start.router)
    dp.include_router(echo.router)

    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
