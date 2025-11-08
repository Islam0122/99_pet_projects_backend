from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.books import create_user_book
from api.telegramusers import get_telegram_user
from keyboards.inline_keyboards import return_menu_kb
import os
import logging

add_book_router = Router()
logger = logging.getLogger(__name__)


class AddBookStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_file = State()


def get_cancel_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ]
    )


@add_book_router.callback_query(F.data == "add_my_books")
async def add_my_book_start(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(bot_message_id=callback.message.message_id)

    await callback.message.edit_caption(
        caption=(
            "📘 <b>Добавление книги</b>\n\n"
            "Введите название книги:"
        ),
        reply_markup=get_cancel_kb(),
        parse_mode="HTML"
    )
    await state.set_state(AddBookStates.waiting_for_title)
    await callback.answer()


@add_book_router.message(AddBookStates.waiting_for_title)
async def add_book_title(message: types.Message, state: FSMContext, bot: Bot):
    title = message.text.strip()

    if not title:
        await message.answer("❗ Название не может быть пустым. Введите название книги:")
        return

    if len(title) > 200:
        await message.answer("❗ Название слишком длинное. Максимум 200 символов. Введите название снова:")
        return

    await state.update_data(title=title)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')

    await message.delete()

    await bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=bot_message_id,
        caption=(
            "📘 <b>Добавление книги</b>\n\n"
            f"✅ <b>Название:</b> {title}\n"
            "📝 Введите описание книги:"
        ),
        reply_markup=get_cancel_kb(),
        parse_mode="HTML"
    )
    await state.set_state(AddBookStates.waiting_for_description)


@add_book_router.message(AddBookStates.waiting_for_description)
async def add_book_description(message: types.Message, state: FSMContext, bot: Bot):
    description = message.text.strip()

    if not description:
        await message.answer("❗ Описание не может быть пустым. Введите описание книги:")
        return

    if len(description) > 1000:
        await message.answer("❗ Описание слишком длинное. Максимум 1000 символов. Введите описание снова:")
        return

    await state.update_data(description=description)

    data = await state.get_data()
    title = data.get("title")
    bot_message_id = data.get('bot_message_id')

    await message.delete()

    await bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=bot_message_id,
        caption=(
            "📘 <b>Добавление книги</b>\n\n"
            f"✅ <b>Название:</b> {title}\n"
            f"✅ <b>Описание:</b> {description[:100]}...\n\n"
            "📄 Прикрепите файл книги (только .txt):"
        ),
        reply_markup=get_cancel_kb(),
        parse_mode="HTML"
    )
    await state.set_state(AddBookStates.waiting_for_file)


@add_book_router.message(AddBookStates.waiting_for_file)
async def add_book_file(message: types.Message, state: FSMContext, bot: Bot):
    if not message.document:
        await message.answer("❗ Пожалуйста, прикрепите файл .txt")
        return

    if not message.document.file_name.lower().endswith(".txt"):
        await message.answer("❗ Только файлы .txt поддерживаются")
        return

    if message.document.file_size > 10 * 1024 * 1024:
        await message.answer("❗ Файл слишком большой. Максимум 10MB")
        return

    if message.document.file_size == 0:
        await message.answer("❗ Файл пустой. Прикрепите файл с содержимым.")
        return

    data = await state.get_data()
    title = data.get("title")
    description = data.get("description")
    bot_message_id = data.get('bot_message_id')

    await message.delete()

    await bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=bot_message_id,
        caption=(
            "📘 <b>Добавление книги</b>\n\n"
            f"✅ <b>Название:</b> {title}\n"
            f"✅ <b>Описание:</b> {description[:100]}...\n"
            f"✅ <b>Файл:</b> {message.document.file_name}\n\n"
            "⏳ <i>Обрабатываю файл...</i>"
        ),
        reply_markup=None,
        parse_mode="HTML"
    )

    os.makedirs("temp_uploads", exist_ok=True)
    unique_filename = f"{message.from_user.id}_{message.message_id}.txt"
    temp_file_path = f"temp_uploads/{unique_filename}"

    try:
        await bot.download(message.document, destination=temp_file_path)

        if not os.path.exists(temp_file_path) or os.path.getsize(temp_file_path) == 0:
            raise Exception("Файл не был скачан или пустой")

        file_size = os.path.getsize(temp_file_path)
        logger.info(f"Файл скачан: {message.document.file_name}, размер: {file_size} байт")

    except Exception as e:
        logger.error(f"Ошибка при скачивании файла: {e}")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        await bot.edit_message_caption(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            caption=(
                "📘 <b>Добавление книги</b>\n\n"
                f"✅ <b>Название:</b> {title}\n"
                f"✅ <b>Описание:</b> {description[:100]}...\n\n"
                "❌ <b>Ошибка:</b> Не удалось скачать файл"
            ),
            reply_markup=get_cancel_kb(),
            parse_mode="HTML"
        )
        return

    try:
        user_data = await get_telegram_user(message.from_user.id)
        telegram_user_id = user_data['id']
    except Exception as e:
        logger.error(f"Ошибка при получении данных пользователя: {e}")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        await bot.edit_message_caption(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            caption=(
                "📘 <b>Добавление книги</b>\n\n"
                f"✅ <b>Название:</b> {title}\n"
                f"✅ <b>Описание:</b> {description[:100]}...\n\n"
                "❌ <b>Ошибка:</b> Проблема с данными пользователя"
            ),
            reply_markup=return_menu_kb(),
            parse_mode="HTML"
        )
        await state.clear()
        return

    try:
        with open(temp_file_path, 'rb') as file:
            result = await create_user_book(
                title=title,
                description=description,
                telegram_user_id=telegram_user_id,
                file=file,
                file_name=message.document.file_name
            )

        if result:
            await bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=bot_message_id,
                caption=(
                    "📘 <b>Добавление книги</b>\n\n"
                    f"✅ <b>Название:</b> {title}\n"
                    f"✅ <b>Описание:</b> {description[:100]}...\n"
                    f"✅ <b>Файл:</b> {message.document.file_name}\n\n"
                    "🎉 <b>Книга успешно добавлена!</b>"
                ),
                reply_markup=return_menu_kb(),
                parse_mode="HTML"
            )
            logger.info(f"Книга '{title}' успешно добавлена пользователем {message.from_user.id}")
        else:
            await bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=bot_message_id,
                caption=(
                    "📘 <b>Добавление книги</b>\n\n"
                    f"✅ <b>Название:</b> {title}\n"
                    f"✅ <b>Описание:</b> {description[:100]}...\n\n"
                    "❌ <b>Ошибка:</b> Не удалось сохранить книгу"
                ),
                reply_markup=get_cancel_kb(),
                parse_mode="HTML"
            )

    except Exception as e:
        logger.error(f"Ошибка при сохранении книги: {e}")
        await bot.edit_message_caption(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            caption=(
                "📘 <b>Добавление книги</b>\n\n"
                f"✅ <b>Название:</b> {title}\n"
                f"✅ <b>Описание:</b> {description[:100]}...\n\n"
                "❌ <b>Ошибка:</b> Ошибка сервера"
            ),
            reply_markup=get_cancel_kb(),
            parse_mode="HTML"
        )

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        await state.clear()


@add_book_router.callback_query(F.data == "cancel")
async def cancel_add_book(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await callback.message.edit_caption(
        caption="❌ <b>Добавление книги отменено</b>",
        reply_markup=return_menu_kb(),
        parse_mode="HTML"
    )
    await callback.answer()