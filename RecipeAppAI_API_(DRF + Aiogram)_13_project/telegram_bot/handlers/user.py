from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery,FSInputFile
from external_services.api_client_user import TgUserAPI
from lexicon.lexicon_ru import LEXICON_RU
from lexicon.lexicon_en import LEXICON_EN
from keyboards.inline_keyboards import inline_language_keyboard,inline_language_keyboard2, get_main_menu, get_cancel_keyboard

user_router = Router()
photo = FSInputFile("img.png")

from datetime import datetime

def format_date(date_str: str, language: str = "en") -> str:
    """
    Преобразует ISO дату в красивый вид.
    date_str: строка ISO формата, например '2025-09-21T18:16:52.950Z'
    language: 'ru' или 'en'
    """
    try:
        # Убираем Z в конце, если есть
        if date_str.endswith("Z"):
            date_str = date_str[:-1]
        dt = datetime.fromisoformat(date_str)
        if language == "ru":
            return dt.strftime("%d %b %Y, %H:%M")  # 21 Сен 2025, 18:16
        else:
            return dt.strftime("%d %b %Y, %H:%M")  # 21 Sep 2025, 18:16
    except Exception:
        return date_str


# ------------- start
@user_router.message(Command("start"))
async def cmd_start(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username or "Unknown"
    full_name = message.from_user.full_name or "Unknown"

    async with TgUserAPI() as api:
        user = await api.get_user_by_telegram_id(telegram_id)

        if user:
            await api.create_or_update_user(
                username=username,
                full_name=full_name,
                telegram_id=telegram_id,
                language=user.get("language", "ru")
            )
            lang = user.get("language", "ru")
            lexicon = LEXICON_EN if lang == "en" else LEXICON_RU
            greeting_text = (
                f"👋 {lexicon['greeting']}\n\n"
                f"📌 {lexicon['start_help']}"
            )
            await message.answer_photo(
                photo=photo,
                caption=greeting_text,
                reply_markup=get_main_menu(lang),
                parse_mode="Markdown"
            )
        else:
            await message.answer(
                "🌐 Выберите язык / Choose your language:",
                reply_markup=inline_language_keyboard()
            )

@user_router.callback_query(lambda c: c.data == "menu:main")
async def return_to_main_menu(callback: CallbackQuery):
    telegram_id = callback.from_user.id

    async with TgUserAPI() as api:
        user = await api.get_user_by_telegram_id(telegram_id)
    lang = user.get("language", "ru") if user else "ru"
    lexicon = LEXICON_EN if lang == "en" else LEXICON_RU
    greeting_text = (
        f"👋 {lexicon['greeting']}\n\n"
        f"📌 {lexicon['start_help']}"
    )

    await callback.message.edit_caption(
        caption=greeting_text,
        reply_markup=get_main_menu(lang),
        parse_mode="Markdown"
    )
    await callback.answer()

# ------------- help
@user_router.message(Command("help"))
async def cmd_help(message: types.Message):
    telegram_id = message.from_user.id
    async with TgUserAPI() as api:
        user = await api.get_user_by_telegram_id(telegram_id)
        if user:
            language = user.get("language", "ru")
        else:
            language = "ru"  # По умолчанию русский

    lexicon = LEXICON_EN if language == "en" else LEXICON_RU
    help_text = (
        f"📌 {lexicon['help_text']}"
    )
    await message.answer_photo(
        photo=photo,
        caption=help_text,
        parse_mode="Markdown"
    )

@user_router.callback_query(lambda c: c.data == "menu:help")
async def menu_help(callback: CallbackQuery):
    telegram_id = callback.from_user.id

    async with TgUserAPI() as api:
        user = await api.get_user_by_telegram_id(telegram_id)
        lang = user.get("language", "ru") if user else "ru"

    lexicon = LEXICON_EN if lang == "en" else LEXICON_RU
    await callback.message.edit_caption(
        caption=lexicon["help_text"],
        reply_markup=get_cancel_keyboard(lang)

    )


# -------------- about
@user_router.message(Command("about"))
async def cmd_about(message: types.Message):
    telegram_id = message.from_user.id
    async with TgUserAPI() as api:
        user = await api.get_user_by_telegram_id(telegram_id)
        language = user.get("language", "ru") if user else "ru"

    lexicon = LEXICON_EN if language == "en" else LEXICON_RU
    about_text = (
        f"📌 {lexicon['about_text']}"
    )
    await message.answer_photo(
        photo=photo,
        caption=about_text,
    )

@user_router.callback_query(lambda c: c.data == "menu:about")
async def menu_about(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    async with TgUserAPI() as api:
        user = await api.get_user_by_telegram_id(telegram_id)
        lang = user.get("language", "ru") if user else "ru"

    lexicon = LEXICON_EN if lang == "en" else LEXICON_RU
    await callback.message.edit_caption(
        caption=f"📌 {lexicon['about_text']}",
        reply_markup=get_cancel_keyboard(lang)

    )



@user_router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    telegram_id = message.from_user.id

    async with TgUserAPI() as api:
        user = await api.get_user_by_telegram_id(telegram_id)
        if user:
            language = user.get("language", "ru")
            username = user.get("username", "Unknown")
            username_with_at = user.get("username_with_at", f"@{username}")
            full_name = user.get("full_name", "Unknown")
            telegram_id_str = user.get("telegram_id", "Unknown")
            created_at = user.get("created_at", "Unknown")
            joined_at = user.get("joined_at", "Unknown")
        else:
            language = "ru"
            username = username_with_at = full_name = telegram_id_str = created_at = joined_at = "Unknown"

    lexicon = LEXICON_EN if language == "en" else LEXICON_RU
    created_at_fmt = format_date(created_at, language)
    joined_at_fmt = format_date(joined_at, language)
    if language == "ru":
        profile_text = (
            f"👤 {lexicon.get('profile_title', 'Ваш профиль')}\n\n"
            f"📝 Юзернейм: {username_with_at}\n"
            f"📛 Полное имя: {full_name}\n"
            f"🆔 Telegram ID: {telegram_id_str}\n"
            f"📅 Дата создания: {created_at_fmt}\n"
            f"📌 Дата присоединения: {joined_at_fmt}\n\n"
            f"ℹ️ {lexicon.get('profile_help', 'Здесь вы можете просмотреть свой профиль, историю и любимые рецепты.')}"
        )
    else:
        profile_text = (
            f"👤 {lexicon.get('profile_title', 'Your Profile')}\n\n"
            f"📝 Username: {username_with_at}\n"
            f"📛 Full Name: {full_name}\n"
            f"🆔 Telegram ID: {telegram_id_str}\n"
            f"📅 Created At: {created_at_fmt}\n"
            f"📌 Joined At: {joined_at_fmt}\n\n"
            f"ℹ️ {lexicon.get('profile_help', 'Here you can view your profile, history, and favorite recipes.')}"
        )

    await message.answer_photo(
        photo=photo,
        caption=profile_text,
    )


# ------- select language
@user_router.callback_query(lambda c: c.data == "menu:language")
async def open_language_menu(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption="🌐 Выберите язык / Choose your language:",
        reply_markup=inline_language_keyboard2()
    )
    await callback.answer()

@user_router.callback_query(lambda c: c.data and c.data.startswith("set_lang:"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    telegram_id = callback.from_user.id
    username = callback.from_user.username or "Unknown"
    full_name = callback.from_user.full_name or "Unknown"

    async with TgUserAPI() as api:
        await api.create_or_update_user(
            username=username,
            full_name=full_name,
            telegram_id=telegram_id,
            language=lang
        )

    lexicon = LEXICON_EN if lang == "en" else LEXICON_RU
    greeting_text = (
        f"👋 {lexicon['greeting']}\n\n"
        f"📌 {lexicon['start_help']}"
    )
    await callback.message.answer(greeting_text, parse_mode="Markdown")
    await callback.answer()

@user_router.callback_query(lambda c: c.data and c.data.startswith("set_lang2:"))
async def set_language2(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    telegram_id = callback.from_user.id
    username = callback.from_user.username or "Unknown"
    full_name = callback.from_user.full_name or "Unknown"

    async with TgUserAPI() as api:
        await api.create_or_update_user(
            username=username,
            full_name=full_name,
            telegram_id=telegram_id,
            language=lang
        )

    lexicon = LEXICON_EN if lang == "en" else LEXICON_RU
    greeting_text = (
        f"👋 {lexicon['greeting']}\n\n"
        f"📌 {lexicon['start_help']}"
    )

    await callback.message.edit_caption(
        caption=greeting_text,
        reply_markup=get_main_menu(lang),
        parse_mode="Markdown"
    )
    await callback.answer("✅ Язык изменён")