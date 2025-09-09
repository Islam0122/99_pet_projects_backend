import asyncio
from aiogram import Bot,Dispatcher

from database.database import init_db
from admin_handlers import admin_router
from handlers import *

TOKEN = "8227707236:AAFlQlr8OvklYp9v8hbOvOkQ3FaTimbpVhQ"
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router)
dp.include_router(admin_router)

async def startup():
    print("----------------------- i woke up BOSS ---------------------------")

async def off():
    print(" ----------------------i asleep BOSS -----------------------------")

async def main():
    await init_db()
    dp.startup.register(startup)
    dp.shutdown.register(off)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())