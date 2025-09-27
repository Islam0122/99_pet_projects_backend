import json
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery,FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from external_services.api_client_user import TgUserAPI
from external_services.api_client_recipe import APIClient
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
            await message.answer_photo(
                photo=photo,
                caption="🌐 Выберите язык / Choose your language:",
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

# ----------- profile
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
            f"ℹ️ {lexicon.get('profile_help',)}"
        )
    else:
        profile_text = (
            f"👤 {lexicon.get('profile_title', 'Your Profile')}\n\n"
            f"📝 Username: {username_with_at}\n"
            f"📛 Full Name: {full_name}\n"
            f"🆔 Telegram ID: {telegram_id_str}\n"
            f"📅 Created At: {created_at_fmt}\n"
            f"📌 Joined At: {joined_at_fmt}\n\n"
            f"ℹ️ {lexicon.get('profile_help', )}"
        )

    await message.answer_photo(
        photo=photo,
        caption=profile_text,
    )

@user_router.callback_query(lambda c: c.data == "menu:profile")
async def callback_profile(callback: CallbackQuery):
    telegram_id = callback.from_user.id

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
            f"ℹ️ {lexicon.get('profile_help',)}"
        )
        kb = InlineKeyboardBuilder()
        kb.button(text="⬅️ В меню", callback_data="menu:main")
    else:
        profile_text = (
            f"👤 {lexicon.get('profile_title', 'Your Profile')}\n\n"
            f"📝 Username: {username_with_at}\n"
            f"📛 Full Name: {full_name}\n"
            f"🆔 Telegram ID: {telegram_id_str}\n"
            f"📅 Created At: {created_at_fmt}\n"
            f"📌 Joined At: {joined_at_fmt}\n\n"
            f"ℹ️ {lexicon.get('profile_help', )}"
        )
        kb = InlineKeyboardBuilder()
        kb.button(text="⬅️ Back to menu", callback_data="menu:main")

    kb.adjust(1)

    await callback.message.edit_caption(
        caption=profile_text,
        reply_markup=kb.as_markup(),
    )
    await callback.answer()

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
    await callback.message.edit_caption(
        caption=greeting_text, parse_mode="Markdown")
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

# -------------- recipe
# 1. Популярные рецепты -> список категорий
@user_router.callback_query(lambda c: c.data == "menu:popular_recipes")
async def menu_popular_categories(callback: CallbackQuery):
    telegram_id = callback.from_user.id

    # Получаем язык пользователя
    async with TgUserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(telegram_id)
        lang = user.get("language", "ru") if user else "ru"

    lexicon = LEXICON_EN if lang == "en" else LEXICON_RU
    async with APIClient() as api:
        categories = await api.get_categories()

    if not categories:
        await callback.message.answer("❌ " + ("Categories not found." if lang == "en" else "Категории не найдены."))
        await callback.answer()
        return
    kb = InlineKeyboardBuilder()
    for cat in categories:
        kb.button(
            text=cat.get("name", "No name" if lang == "en" else "Без названия"),
            callback_data=f"popular:category:{cat['id']}"
        )
    if lang == "en":
        kb.button(text="⬅️ Back to menu", callback_data="menu:main")
    else:
        kb.button(text="⬅️ В меню", callback_data="menu:main")
    kb.adjust(1)

    kb.adjust(2)

    await callback.message.edit_caption(
        caption="📂 " + ("Choose a category:" if lang == "en" else "Выберите категорию:"),
        reply_markup=kb.as_markup(),
    )
    await callback.answer()

# 2. Выбор категории -> список рецептов
@user_router.callback_query(lambda c: c.data.startswith("popular:category:"))
async def popular_recipes_by_category(callback: CallbackQuery):
    category_id = callback.data.split(":")[2]
    telegram_id = callback.from_user.id

    # Определяем язык пользователя
    async with TgUserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(telegram_id)
        lang = user.get("language", "ru") if user else "ru"

    lexicon = LEXICON_EN if lang == "en" else LEXICON_RU

    # Получаем популярные рецепты
    async with APIClient() as api:
        recipes_data = await api.get_recipes_by_category(category_id=category_id)

    # Проверяем тип данных и фильтруем по категории
    recipes = recipes_data.get("results", [])

    if not recipes:
        msg = "🍽 No popular recipes in this category yet." if lang == "en" else "🍽 В этой категории пока нет популярных рецептов."
        await callback.message.answer(msg)
        await callback.answer()
        return

    # Формируем inline-кнопки для рецептов
    kb = InlineKeyboardBuilder()
    for r in recipes:
        recipe_title = r.get("title", "No name" if lang == "en" else "Без названия")
        kb.button(
            text=recipe_title,
            callback_data=f"popular:recipe:{r['id']}"
        )
    if lang == "en":
        kb.button(text="⬅️ Back to menu", callback_data="menu:main")
    else:
        kb.button(text="⬅️ В меню", callback_data="menu:main")
    kb.adjust(1)

    caption = "🍴 Choose a recipe:" if lang == "en" else "🍴 Выберите рецепт:"
    await callback.message.edit_caption(
        caption=caption,
        reply_markup=kb.as_markup()
    )
    await callback.answer()

# 3. Детальная карточка рецепта
@user_router.callback_query(lambda c: c.data.startswith("popular:recipe:"))
async def popular_recipe_detail(callback: CallbackQuery):
    recipe_id = callback.data.split(":")[2]
    telegram_id = callback.from_user.id

    # Определяем язык пользователя
    async with TgUserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(telegram_id)
        lang = user.get("language", "ru") if user else "ru"

    # Запрос на бэкенд
    async with APIClient() as api:
        recipe = await api._get(f"recipes/{recipe_id}/")

    if not recipe:
        msg = "❌ Recipe not found." if lang == "en" else "❌ Рецепт не найден."
        await callback.message.edit_caption(caption=msg)
        await callback.answer()
        return

    # Данные
    title = recipe.get("title", "No name" if lang == "en" else "Без названия")
    desc = recipe.get("description", "")
    ingredients = recipe.get("ingredients", "—")
    instructions = recipe.get("instructions", "—")

    # Локализация текста
    caption = (
        f"🍲 *{title}*\n\n"
        f"📝 {desc}\n\n"
        f"🥗 *{'Ingredients' if lang == 'en' else 'Ингредиенты'}:*\n{ingredients}\n\n"
        f"👨‍🍳 *{'Instructions' if lang == 'en' else 'Шаги приготовления'}:*\n{instructions}"
    )

    # Клавиатура
    kb = InlineKeyboardBuilder()
    if lang == "en":
        kb.button(text="⬅️ Back to menu", callback_data="menu:main")
    else:
        kb.button(text="⬅️ В меню", callback_data="menu:main")

    await callback.message.edit_caption(
        caption=caption,
        parse_mode="Markdown",
        reply_markup=kb.as_markup()
    )
    await callback.answer()


