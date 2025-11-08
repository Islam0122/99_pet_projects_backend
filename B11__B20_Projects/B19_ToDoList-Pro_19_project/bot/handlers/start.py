from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from keyboards.inline_keyboards import main_menu_kb
from api.telegramusers import create_or_update_telegram_user
from aiogram.filters import Command

start_router = Router()

@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await create_or_update_telegram_user(message.from_user.id, message.from_user.username)
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "Я твой персональный ToDo-бот.\n\n"
        "Вот что ты можешь сделать:\n"
        "• 📋 Посмотреть свои задачи\n"
        "• ✅ Просмотреть завершённые задачи\n"
        "• 👤 Открыть профиль\n"
        "Выбери действие из меню ниже 👇",
        reply_markup=main_menu_kb()
    )

@start_router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text=f"👋 Привет, {callback.message.from_user.first_name}!\n\n"
        "Я твой персональный ToDo-бот.\n\n"
        "Вот что ты можешь сделать:\n"
        "• 📋 Посмотреть свои задачи\n"
        "• ✅ Просмотреть завершённые задачи\n"
        "• 👤 Открыть профиль\n"
        "Выбери действие из меню ниже 👇",
        reply_markup=main_menu_kb()
    )