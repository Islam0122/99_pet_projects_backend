from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from keyboards.inline_keyboards import main_menu_kb, return_menu_kb
from api.telegramusers import create_or_update_telegram_user
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await create_or_update_telegram_user(message.from_user.id, message.from_user.username)

    text = f"""
👋 Привет! Добро пожаловать в Readify — твой персональный помощник в мире книг!

📖 Читай книги,
⚡ Получай XP и повышай уровень,
🔥 Следи за серией дней подряд,
🏆 Соревнуйся с друзьями в топе читателей.

✨ Чтение стало увлекательным и мотивирующим! Начни свой путь к званию Легенда чтения прямо сейчас!
"""
    await message.answer(text, reply_markup=main_menu_kb())


# ------------------ Главное меню ------------------
@start_router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    text = f"""
👋 Привет! Добро пожаловать в Readify — твой персональный помощник в мире книг!

📖 Читай книги,
⚡ Получай XP и повышай уровень,
🔥 Следи за серией дней подряд,
🏆 Соревнуйся с друзьями в топе читателей.

✨ Чтение стало увлекательным и мотивирующим! Начни свой путь к званию Легенда чтения прямо сейчас!
"""
    await callback.message.edit_text(text=text, reply_markup=main_menu_kb())


