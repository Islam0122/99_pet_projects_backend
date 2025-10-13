from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧑 Профиль", callback_data="profile")],
            [InlineKeyboardButton(text="🏆 Топ XP", callback_data="top_xp")]
        ]
    )

def return_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu")]
        ]
    )
