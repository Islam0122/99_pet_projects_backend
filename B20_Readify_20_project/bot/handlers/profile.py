from aiogram import Router, types, F
from api.telegramusers import get_telegram_user, get_top_users
from aiogram.filters import Command
from keyboards.inline_keyboards import return_menu_kb
from datetime import datetime

profile_router = Router()


def format_date(date_str):
    """Преобразует дату из API в красивый формат"""
    if not date_str:
        return "—"
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d.%m.%Y, %H:%M")
    except:
        return date_str  # если формат неизвестен, возвращаем как есть


# ------------------ Команда /profile ------------------
@profile_router.message(Command("profile"))
async def show_profile(message: types.Message):
    user_data = await get_telegram_user(message.from_user.id)
    if not user_data:
        await message.answer("❌ Пользователь не найден.")
        return

    username = user_data.get("username") or message.from_user.username or message.from_user.id
    streak_days = user_data.get("streak_days", 0)
    streak_status = user_data.get("streak_status", "Не начинал streak 🌱")
    total_read_books = user_data.get("total_read_books", 0)
    xp = user_data.get("xp", 0)
    level = user_data.get("level", 1)
    rank = user_data.get("rank", "Новичок")
    last_read_date = format_date(user_data.get("last_read_date"))
    last_active = format_date(user_data.get("last_active"))
    member_since = format_date(user_data.get("member_since"))

    text = (
        f"👤 <b>Профиль @{username}</b>\n\n"
        f"🔥 <b>Streak:</b> {streak_status} ({streak_days} дней подряд)\n"
        f"📚 <b>Прочитано книг:</b> {total_read_books}\n\n"
        f"⚡ <b>Опыт (XP):</b> {xp}\n"
        f"🏅 <b>Уровень:</b> {level}\n"
        f"🎖 <b>Звание:</b> {rank}\n\n"
        f"📖 <b>Последнее прочтение:</b> {last_read_date}\n"
        f"🕓 <b>Последняя активность:</b> {last_active}\n"
        f"📌 <b>В системе с:</b> {member_since}"
    )

    await message.answer(text, reply_markup=return_menu_kb(), parse_mode="HTML")


# ------------------ Кнопка Профиль ------------------
@profile_router.callback_query(F.data == "profile")
async def show_profile_callback(callback: types.CallbackQuery):
    user_data = await get_telegram_user(callback.from_user.id)
    if not user_data:
        await callback.message.answer("❌ Пользователь не найден.")
        return

    username = user_data.get("username") or callback.from_user.username or callback.from_user.id
    streak_days = user_data.get("streak_days", 0)
    streak_status = user_data.get("streak_status", "Не начинал streak 🌱")
    total_read_books = user_data.get("total_read_books", 0)
    xp = user_data.get("xp", 0)
    level = user_data.get("level", 1)
    rank = user_data.get("rank", "Новичок")
    last_read_date = format_date(user_data.get("last_read_date"))
    last_active = format_date(user_data.get("last_active"))
    member_since = format_date(user_data.get("member_since"))

    text = (
        f"👤 <b>Профиль @{username}</b>\n\n"
        f"🔥 <b>Streak:</b> {streak_status} ({streak_days} дней подряд)\n"
        f"📚 <b>Прочитано книг:</b> {total_read_books}\n\n"
        f"⚡ <b>Опыт (XP):</b> {xp}\n"
        f"🏅 <b>Уровень:</b> {level}\n"
        f"🎖 <b>Звание:</b> {rank}\n\n"
        f"📖 <b>Последнее прочтение:</b> {last_read_date}\n"
        f"🕓 <b>Последняя активность:</b> {last_active}\n"
        f"📌 <b>В системе с:</b> {member_since}"
    )

    await callback.message.edit_text(text, reply_markup=return_menu_kb(), parse_mode="HTML")
    await callback.answer()


@profile_router.callback_query(F.data == "top_xp")
async def top_xp(callback: types.CallbackQuery):
    try:
        users = await get_top_users(limit=10)
        if not users:
            await callback.message.answer("Пока нет пользователей в топе 😢")
            return

        text = "🏆 Топ-10 читателей Readify:\n\n"
        for i, user in enumerate(users, start=1):
            text += (
                f"{i}. {user.get('username') or user.get('telegram_id')}\n"
                f"   Уровень: {user.get('level')}, {user.get('rank')}\n"
                f"   XP: {user.get('xp')}, Стрик: {user.get('streak_status')}\n"
                f"   С нами с: {user.get('member_since')}\n\n"
            )

        await callback.message.edit_text(text=text, reply_markup=return_menu_kb())

    except Exception as e:
        await callback.message.answer(text=f"Ошибка при получении топа !!")