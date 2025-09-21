from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


def inline_language_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора языка"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang:en")]
    ])