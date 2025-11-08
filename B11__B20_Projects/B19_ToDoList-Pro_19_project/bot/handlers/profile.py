from aiogram import Router, types, F
from api.telegramusers import get_telegram_user
from aiogram.filters import Command
from keyboards.inline_keyboards import return_menu_kb
profile_router = Router()


@profile_router.message(Command("profile"))
async def show_profile(message: types.Message):
    user_list = await get_telegram_user(message.from_user.id)
    if not user_list:
        await message.answer("❌ Пользователь не найден.")
        return
    user_data = user_list

    streak_days = user_data.get("streak_days", 0)
    streak_status = user_data.get("streak_status", "Не начинал streak 🌱")
    total_completes = user_data.get("total_task_completes", 0)
    member_since = user_data.get("member_since", "Неизвестно")

    text = (
        f"👤 Профиль @{user_data.get('username', '')}\n\n"
        f"🔥 Статус streak: {streak_status}\n"
        f"📅 Количество дней подряд: {streak_days}\n"
        f"✅ Всего выполнено задач: {total_completes}\n"
        f"📌 В системе с: {member_since}"
    )

    await message.answer(text)



@profile_router.callback_query(F.data == "profile")
async def show_profile_callback(callback: types.CallbackQuery):
    user_data = await get_telegram_user(callback.from_user.id)

    if not user_data:
        await callback.message.answer("❌ Пользователь не найден.")
        return

    streak_days = user_data.get("streak_days") or 0
    streak_status = user_data.get("streak_status") or "Не начинал streak 🌱"
    total_completes = user_data.get("total_task_completes") or 0
    member_since = user_data.get("member_since") or "Неизвестно"
    username = user_data.get("username") or "Пользователь"

    text = (
        f"👤 Профиль @{username}\n\n"
        f"🔥 Статус streak: {streak_status}\n"
        f"📅 Количество дней подряд: {streak_days}\n"
        f"✅ Всего выполнено задач: {total_completes}\n"
        f"📌 В системе с: {member_since}"
    )

    await callback.message.edit_text(text,reply_markup=return_menu_kb())
    await callback.answer()
