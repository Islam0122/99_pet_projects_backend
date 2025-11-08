from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def inline_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора языка"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang:en")]
    ])

def inline_language_keyboard2() -> InlineKeyboardMarkup:
    """Клавиатура для выбора языка"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang2:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang2:en")]
    ])

def get_main_menu(lang: str):
    kb = InlineKeyboardBuilder()
    if lang == "en":
        kb.button(text="📤 Popular Recipes", callback_data="menu:popular_recipes")

        kb.button(text="ℹ️ About", callback_data="menu:about")
        kb.button(text="❓ Help", callback_data="menu:help")

        kb.button(text="🤖 Generate Recipe (AI)", callback_data="menu:generate_recipe")

        kb.button(text="👤 Profile", callback_data="menu:profile")

        kb.button(text="🌐 Change language", callback_data="menu:language")
    else:
        kb.button(text="📤 Популярные рецепты", callback_data="menu:popular_recipes")

        kb.button(text="ℹ️ О боте", callback_data="menu:about")
        kb.button(text="❓ Помощь", callback_data="menu:help")

        kb.button(text="🤖 Сгенерировать рецепт (AI)", callback_data="menu:generate_recipe")

        kb.button(text="👤 Профиль", callback_data="menu:profile")

        kb.button(text="🌐 Сменить язык", callback_data="menu:language")

    kb.adjust(1,2,1,1,1)  # кнопки по 2 в ряд
    return kb.as_markup()

def get_cancel_keyboard(lang: str):
    kb = InlineKeyboardBuilder()
    if lang == "en":
        kb.button(text="👤 Profile", callback_data="menu:profile")
        kb.button(text="🌐 Change language", callback_data="menu:language")
        kb.button(text="↩️ Return to menu", callback_data="menu:main")
    else:
        kb.button(text="👤 Профиль", callback_data="menu:profile")
        kb.button(text="🌐 Сменить язык", callback_data="menu:language")
        kb.button(text="↩️ Вернуться в меню", callback_data="menu:main")

    kb.adjust(2, 1)  # первые 2 в ряд, последняя отдельной строкой
    return kb.as_markup()