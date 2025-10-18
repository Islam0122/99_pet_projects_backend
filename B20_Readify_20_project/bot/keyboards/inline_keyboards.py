from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🧑 Профиль", callback_data="profile"),
                InlineKeyboardButton(text="🏆 Топ XP", callback_data="top_xp")
            ],
            [
                InlineKeyboardButton(text="📖 Мои книги", callback_data="users_books"),
                InlineKeyboardButton(text="📚 Библиотека", callback_data="library")
            ],
            [
                InlineKeyboardButton(text="🔍 Найти книгу", callback_data="search_book"),
            ],
            [
                InlineKeyboardButton(text="🤖 AI Help", callback_data="ai_help")
            ],
            [
                InlineKeyboardButton(text="ℹ️ О боте", callback_data="about_bot"),
                InlineKeyboardButton(text="🚀 Скоро: Readify 2.0", callback_data="soon_update")
            ],
            [
                InlineKeyboardButton(text="➕ Добавить свою книгу", callback_data="add_my_books"),
            ],
        ]
    )


def return_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu")]
        ]
    )
