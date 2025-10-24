from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu():
    kb = InlineKeyboardBuilder()

    # 🟩 Профиль и рейтинг
    kb.button(text="👤 Профиль", callback_data="menu:profile")
    kb.button(text="📊 Топ студентов", callback_data="menu:top_students")

    # 🟦 Информация
    kb.button(text="ℹ️ О боте", callback_data="menu:about")
    kb.button(text="👨‍🏫 О преподавателе", callback_data="menu:about_teacher")

    # 🗓 План урока
    kb.button(text="📅 План урока", url="https://docs.google.com/spreadsheets/d/1WyWNB3PLRzvBVAa8CRMc5U-Q463lPIPY11ygO1MDMNI/edit?usp=sharing")

    # 🟨 Задания
    kb.button(text="📝 Отправить задание", callback_data="menu:send_task")
    kb.button(text="⏳ Мои задания (не проверены)", callback_data="menu:pending_tasks")
    kb.button(text="✅ Мои задания (проверены)", callback_data="menu:checked_tasks")

    # Настройка рядов: по 2 кнопки в первых двух рядах, остальные по одной
    kb.adjust(2, 2, 1, 1, 1)

    return kb.as_markup()


def get_teacher_account():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="👨‍🏫 Связаться с преподавателем",
        url="https://t.me/islam_duishobaev"
    )
    kb.adjust(1)

    return kb.as_markup()


def return_menu():
    kb = InlineKeyboardBuilder()
    kb.button(
        text="⬅️ Главное меню",
        callback_data="main_menu"
    )
    return kb.as_markup()