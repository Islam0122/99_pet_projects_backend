from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot, language: str = "ru"):
    if language == "en":
        main_menu_commands = [
            BotCommand(command="/start", description="🚀 Start"),
            BotCommand(command="/help", description="❓ Help"),
            BotCommand(command="/about", description="ℹ️ About the project"),
            BotCommand(command="/profile", description="👤 My profile"),
        ]
    else:
        main_menu_commands = [
            BotCommand(command="/start", description="🚀 Начать работу"),
            BotCommand(command="/help", description="❓ Помощь"),
            BotCommand(command="/about", description="ℹ️ О проекте"),
            BotCommand(command="/profile", description="👤 Мой профиль"),
        ]

    await bot.set_my_commands(main_menu_commands)

