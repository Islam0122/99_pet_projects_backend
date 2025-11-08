from aiogram import Router, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from keyboards import admin_main_keyboard, admin_back_keyboard
from datetime import datetime, timedelta
from sqlalchemy import select, func
from database.models import User
from database.database import async_session

admin_router = Router()

admins_list = [7228221648]

@admin_router.message(F.text == "/start_admin")
async def admin_start(message: Message):
    if message.from_user.id in admins_list:
        await message.answer_photo(
            photo=FSInputFile("images/image.png"),
            caption="👨‍💻 *Добро пожаловать в админ-панель!*\n\n"
                    "Выберите нужное действие ниже ⬇️",
            reply_markup=admin_main_keyboard,
            parse_mode="Markdown"
        )
    else:
        await message.answer("⛔️ Эта команда вам недоступна.")


@admin_router.callback_query(F.data == "admin_stats")
async def show_stats(callback: CallbackQuery):
    async with async_session() as session:
        now = datetime.utcnow()

        total_users = (await session.execute(select(func.count(User.id)))).scalar()
        enroll_clicks = (await session.execute(
            select(func.count(User.id)).where(User.clicked_enroll == True)
        )).scalar()
        active_week = (await session.execute(
            select(func.count(User.id)).where(User.last_activity >= now - timedelta(days=7))
        )).scalar()
        active_month = (await session.execute(
            select(func.count(User.id)).where(User.last_activity >= now - timedelta(days=30))
        )).scalar()

    text = (
        "📊 *Статистика*\n\n"
        f"👤 Всего пользователей: *{total_users}*\n"
        f"🚀 Нажали 'Записаться': *{enroll_clicks}*\n"
        f"📅 Активны за неделю: *{active_week}*\n"
        f"🗓 Активны за месяц: *{active_month}*\n\n"
    )

    await callback.message.edit_caption(
        caption=text,
        parse_mode="Markdown",
        reply_markup=admin_back_keyboard
    )


@admin_router.callback_query(F.data == "admin_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption="👨‍💻 *Добро пожаловать в админ-панель!*\n\n"
                "Выберите нужное действие ниже ⬇️",
        parse_mode="Markdown",
        reply_markup=admin_main_keyboard
    )
