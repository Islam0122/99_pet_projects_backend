import asyncio
from aiogram import Bot,Dispatcher
from handlers import *

TOKEN = "8227707236:AAFlQlr8OvklYp9v8hbOvOkQ3FaTimbpVhQ"
bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def startup():
    print("----------------------- i woke up BOSS ---------------------------")

async def off():
    print(" ----------------------i asleep BOSS -----------------------------")

async def main():
    dp.startup.register(startup)
    dp.shutdown.register(off)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())