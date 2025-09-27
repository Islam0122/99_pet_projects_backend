from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from external_services.api_client_recipe import APIClient
from external_services.api_client_user import TgUserAPI
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU
from lexicon.lexicon_en import LEXICON_EN
from keyboards.inline_keyboards import inline_language_keyboard,inline_language_keyboard2, get_main_menu, get_cancel_keyboard

generate_router = Router()

class GenerateRecipeStates(StatesGroup):
    choosing_category = State()
    waiting_for_ingredients = State()

@generate_router.callback_query(F.data == "menu:generate_recipe")
async def generate_recipe_start(callback: CallbackQuery, state: FSMContext):

    async with TgUserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(callback.from_user.id)
        lang = user.get("language", "ru") if user else "ru"

    async with APIClient() as api:
        categories = await api.get_categories()

    kb = InlineKeyboardBuilder()
    for cat in categories:
        kb.button(
            text=cat["name"],
            callback_data=f"choose_category:{cat['id']}"
        )
    if lang == "en":
        text = "Choose a category 🍽️:"
        kb.button(text="⬅️ Back to menu", callback_data="cancel")
    else:
        text = "Выберите категорию 🍽️:"
        kb.button(text="⬅️ В меню", callback_data="cancel")
    kb.adjust(2)

    await callback.message.edit_caption(
        caption=text, reply_markup=kb.as_markup())
    await state.set_state(GenerateRecipeStates.choosing_category)
    await callback.answer()


@generate_router.callback_query(F.data.startswith("choose_category:"))
async def choose_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split(":")[1])
    await state.update_data(category_id=category_id, chat_id=callback.message.chat.id,
                            message_id=callback.message.message_id)
    async with TgUserAPI() as user_api:
        user = await user_api.get_user_by_telegram_id(callback.from_user.id)
        lang = user.get("language", "ru") if user else "ru"

    kb = InlineKeyboardBuilder()
    if lang == "en":
        text = "Now enter ingredients or your preferences 🥦🍅🥩:"
        kb.button(text="⬅️ Back to menu", callback_data="cancel")
    else:
        text = "Теперь введите ингредиенты или пожелания 🥦🍅🥩:"
        kb.button(text="⬅️ В меню", callback_data="cancel")
    kb.adjust(2)

    await callback.message.edit_caption(
        caption=text,
        reply_markup=kb.as_markup()
        )
    await state.set_state(GenerateRecipeStates.waiting_for_ingredients)
    await callback.answer()


@generate_router.message(GenerateRecipeStates.waiting_for_ingredients)
async def generate_recipe_process(message: Message, state: FSMContext, bot: Bot):
    telegram_id = message.from_user.id
    user_text = message.text.strip()

    data = await state.get_data()
    category_id = data.get("category_id")
    chat_id = data.get("chat_id")

    async with TgUserAPI() as api:
        user = await api.get_user_by_telegram_id(telegram_id)
        lang = user.get("language", "ru") if user else "ru"

        if not user:
            await message.answer("Пользователь не найден ❌")
            return

        user_id = user["id"]

    async with APIClient() as api:
        recipe = await api.create_user_recipe(
            user_id=user_id,
            category_id=category_id,
            user_text=user_text
        )

    kb = InlineKeyboardBuilder()
    if lang == "en":
        text = "✨ Here is your recipe:"
        kb.button(text="⬅️ Back to menu", callback_data="cancel")
    else:
        text = "✨ Вот твой рецепт::"
        kb.button(text="⬅️ В меню", callback_data="cancel")
    kb.adjust(2)
    ai_result = recipe.get("ai_result", "AI не вернул рецепт 😢")

    final_text = f"{text}\n\n{ai_result}"
    if len(final_text) <= 1024:
        await bot.edit_message_caption(
            chat_id=chat_id,
            message_id=data["message_id"],
            caption=final_text,
            reply_markup=kb.as_markup()
        )
        await message.delete()
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=final_text,
        )
        await bot.delete_message(
            chat_id=chat_id,
            message_id=data["message_id"]
        )

    await state.clear()


@generate_router.callback_query(lambda c: c.data == "cancel")
async def return_from_generate_to_main_menu(callback: CallbackQuery, state: FSMContext, bot: Bot):
    telegram_id = callback.from_user.id
    await state.clear()

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
