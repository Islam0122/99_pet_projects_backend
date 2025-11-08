from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.books import fetch_user_books, delete_user_book, read_user_book
from api.telegramusers import get_telegram_user, update_user_reading_stats, add_xp_to_user
import logging

user_books_router = Router()
logger = logging.getLogger(__name__)
# photo = "AgACAgIAAxkBAAIBXmjyji-cVZO1zhue4OhyMYaTX9UtAAIL-DEbw-l5S3ATNiEmk1T9AQADAgADeQADNgQ"
photo = "AgACAgIAAxkBAAMDaPKvyEnH5FIT0qqDz0MDw7bDd3EAAgv4MRvD6XlLxL9qsd2EDbkBAAMCAAN5AAM2BA"


def get_user_books_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Мои книги", callback_data="users_books")],
            [InlineKeyboardButton(text="📤 Добавить книгу", callback_data="add_my_books")],
            [InlineKeyboardButton(text="⏪ Назад", callback_data="main_menu")]
        ]
    )


def get_book_actions_kb(book_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Читать", callback_data=f"read_book_{book_id}")],
            [InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_book_{book_id}")],
            [InlineKeyboardButton(text="⏪ Назад к списку", callback_data="users_books")]
        ]
    )


def get_books_pagination_kb(books, page=0, books_per_page=5):
    """Клавиатура с пагинацией для списка книг"""
    start_idx = page * books_per_page
    end_idx = start_idx + books_per_page
    current_books = books[start_idx:end_idx]

    keyboard = []

    # Кнопки для каждой книги
    for book in current_books:
        keyboard.append([
            InlineKeyboardButton(
                text=f"📘 {book['title'][:30]}",
                callback_data=f"book_detail_{book['id']}"
            )
        ])

    # Кнопки пагинации
    pagination_buttons = []

    if page > 0:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"books_page_{page - 1}"))

    # Информация о странице
    total_pages = (len(books) + books_per_page - 1) // books_per_page
    if total_pages > 1:
        pagination_buttons.append(InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="current_page"
        ))

    if end_idx < len(books):
        pagination_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"books_page_{page + 1}"))

    if pagination_buttons:
        keyboard.append(pagination_buttons)

    # Основные кнопки
    keyboard.extend([
        [InlineKeyboardButton(text="📤 Добавить книгу", callback_data="add_my_books")],
        [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@user_books_router.callback_query(F.data == "users_books")
async def show_user_books(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Показать книги пользователя"""
    await state.clear()

    try:
        user_data = await get_telegram_user(callback.from_user.id)
        telegram_user_id = user_data['telegram_id']

        all_books = await fetch_user_books()

        user_books = [
            book for book in all_books
            if book.get('telegram_user') == user_data['id']
        ]

        if not user_books:
            await callback.message.edit_media(
                media=types.InputMediaPhoto(
                    media=photo,
                    caption=(
                        "📖 <b>Мои книги</b>\n\n"
                        "📭 У вас пока нет добавленных книг.\n\n"
                        "Нажмите '📤 Добавить книгу' чтобы добавить свою первую книгу!"
                    ),
                    parse_mode="HTML"
                ),
                reply_markup=get_user_books_kb()
            )
        else:
            await state.update_data(all_user_books=user_books, current_page=0)
            await show_books_page(callback, state, bot)

    except Exception as e:
        logger.error(f"Ошибка при получении книг пользователя: {e}")
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo,
                caption=(
                    "❌ <b>Ошибка</b>\n\n"
                    "Не удалось загрузить ваши книги. Попробуйте позже."
                ),
                parse_mode="HTML"
            ),
            reply_markup=get_user_books_kb()
        )

    await callback.answer()


@user_books_router.callback_query(F.data.startswith("book_detail_"))
async def show_book_detail(callback: types.CallbackQuery, state: FSMContext):
    """Показать детали книги"""
    book_id = int(callback.data.split("_")[2])

    try:
        all_books = await fetch_user_books()
        book = next((b for b in all_books if b['id'] == book_id), None)

        if not book:
            await callback.answer("❌ Книга не найдена")
            return

        book_text = (
            f"📘 <b>{book['title']}</b>\n\n"
            f"📝 <b>Описание:</b>\n{book['description']}\n\n"
            f"📅 <b>Добавлена:</b> {book['created_at'][:10]}\n"
            f"🆔 <b>ID:</b> {book['id']}"
        )

        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo,
                caption=book_text,
                parse_mode="HTML"
            ),
            reply_markup=get_book_actions_kb(book_id)
        )

    except Exception as e:
        logger.error(f"Ошибка при показе деталей книги: {e}")
        await callback.answer("❌ Ошибка при загрузке книги")

    await callback.answer()


@user_books_router.callback_query(F.data.startswith("delete_book_"))
async def delete_book_handler(callback: types.CallbackQuery, state: FSMContext):
    """Удаление книги"""
    book_id = int(callback.data.split("_")[2])
    try:
        # Подтверждение удаления
        confirmation_kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_delete_{book_id}")],
                [InlineKeyboardButton(text="❌ Отмена", callback_data=f"book_detail_{book_id}")]
            ]
        )

        await callback.message.edit_caption(
            caption="⚠️ <b>Подтверждение удаления</b>\n\nВы уверены, что хотите удалить эту книгу?",
            reply_markup=confirmation_kb,
            parse_mode="HTML"
        )

    except Exception as e:
        logger.error(f"Ошибка при подтверждении удаления: {e}")
        await callback.answer("❌ Ошибка")

    await callback.answer()


@user_books_router.callback_query(F.data.startswith("confirm_delete_"))
async def confirm_delete_book(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Подтвержденное удаление книги"""
    book_id = int(callback.data.split("_")[2])
    try:
        await callback.message.edit_caption(
            caption="⏳ <b>Удаляю книгу...</b>",
            reply_markup=None,
            parse_mode="HTML"
        )

        success = await delete_user_book(book_id)

        if success:
            await callback.message.edit_media(
                media=types.InputMediaPhoto(
                    media=photo,
                    caption="✅ <b>Книга успешно удалена!</b>",
                    parse_mode="HTML"
                ),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="📖 Мои книги", callback_data="users_books")],
                        [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
                    ]
                )
            )
        else:
            await callback.message.edit_media(
                media=types.InputMediaPhoto(
                    media=photo,
                    caption="❌ <b>Ошибка</b>\n\nНе удалось удалить книгу.",
                    parse_mode="HTML"
                ),
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="📖 Мои книги", callback_data="users_books")],
                        [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
                    ]
                )
            )

    except Exception as e:
        logger.error(f"Ошибка при удалении книги: {e}")
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo,
                caption="❌ <b>Ошибка</b>\n\nНе удалось удалить книгу.",
                parse_mode="HTML"
            ),
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="📖 Мои книги", callback_data="users_books")],
                    [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
                ]
            )
        )

    await callback.answer()


def get_reading_pagination_kb(book_id: int, current_page: int, total_pages: int, total_xp: int = 0):
    """Клавиатура для пагинации при чтении книги"""
    keyboard = []

    # Кнопки пагинации
    pagination_buttons = []

    if current_page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=f"read_page_{book_id}_{current_page - 1}"))

    # Добавляем информацию о XP
    page_info = f"{current_page + 1}/{total_pages}"
    if total_xp > 0:
        page_info = f"{current_page + 1}/{total_pages} (+{total_xp}XP)"

    pagination_buttons.append(InlineKeyboardButton(
        text=page_info,
        callback_data="current_reading_page"
    ))

    if current_page < total_pages - 1:
        pagination_buttons.append(
            InlineKeyboardButton(text="➡️", callback_data=f"read_page_{book_id}_{current_page + 1}"))

    keyboard.append(pagination_buttons)

    # Основные кнопки
    keyboard.extend([
        [InlineKeyboardButton(text="📖 Содержание", callback_data=f"book_detail_{book_id}")],
        [InlineKeyboardButton(text="⏪ К списку книг", callback_data="users_books")]
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

async def show_books_page(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Показать страницу с книгами"""
    data = await state.get_data()
    user_books = data.get('all_user_books', [])
    current_page = data.get('current_page', 0)
    books_per_page = 5

    total_pages = (len(user_books) + books_per_page - 1) // books_per_page

    # Защита от выхода за границы
    if current_page >= total_pages:
        current_page = total_pages - 1
    if current_page < 0:
        current_page = 0

    await state.update_data(current_page=current_page)

    start_idx = current_page * books_per_page
    end_idx = start_idx + books_per_page
    current_books = user_books[start_idx:end_idx]

    # Формируем текст
    books_text = f"📖 <b>Мои книги</b> (стр. {current_page + 1}/{total_pages})\n\n"

    if not current_books:
        books_text += "📭 На этой странице нет книг."
    else:
        pass
    books_text += f"📚 Всего книг: {len(user_books)}"

    try:
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo,
                caption=books_text,
                parse_mode="HTML"
            ),
            reply_markup=get_books_pagination_kb(user_books, current_page, books_per_page)
        )
    except Exception as e:
        logger.error(f"Ошибка при редактировании сообщения: {e}")
        # Если не удалось отредактировать, отправляем новое
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=photo,
            caption=books_text,
            reply_markup=get_books_pagination_kb(user_books, current_page, books_per_page),
            parse_mode="HTML"
        )


@user_books_router.callback_query(F.data.startswith("books_page_"))
async def handle_books_pagination(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Обработка пагинации книг"""
    page = int(callback.data.split("_")[2])
    await state.update_data(current_page=page)
    await show_books_page(callback, state, bot)
    await callback.answer()


@user_books_router.callback_query(F.data == "current_page")
async def handle_current_page(callback: types.CallbackQuery):
    """Обработка нажатия на номер текущей страницы"""
    await callback.answer("📄 Текущая страница")


@user_books_router.callback_query(F.data.startswith("read_book_"))
async def read_book_handler(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Чтение книги с пагинацией и добавлением XP"""
    book_id = int(callback.data.split("_")[2])

    try:
        # Получаем данные пользователя
        user_data = await get_telegram_user(callback.from_user.id)

        if not user_data:
            await callback.message.edit_media(
                media=types.InputMediaPhoto(
                    media=photo,
                    caption="❌ <b>Ошибка</b>\n\nПользователь не найден.",
                    parse_mode="HTML"
                ),
                reply_markup=get_book_actions_kb(book_id)
            )
            return

        telegram_user_id = user_data['telegram_id']

        await callback.message.edit_caption(
            caption="⏳ <b>Загружаю книгу...</b>",
            reply_markup=None,
            parse_mode="HTML"
        )

        # Получаем содержимое книги
        book_content = await read_user_book(book_id)

        if not book_content:
            await callback.message.edit_media(
                media=types.InputMediaPhoto(
                    media=photo,
                    caption="❌ <b>Ошибка</b>\n\nНе удалось загрузить книгу.",
                    parse_mode="HTML"
                ),
                reply_markup=get_book_actions_kb(book_id)
            )
            return

        content = book_content.get('content', '')
        title = book_content.get('title', 'Книга')

        # Разбиваем на страницы
        MAX_PAGE_LENGTH = 3000
        pages = []
        current_page = ""

        for line in content.split('\n'):
            if len(current_page + line + '\n') <= MAX_PAGE_LENGTH:
                current_page += line + '\n'
            else:
                if current_page:
                    pages.append(current_page.strip())
                current_page = line + '\n'

        if current_page:
            pages.append(current_page.strip())

        if not pages:
            pages = [content]

        # Сохраняем данные о книге в состоянии
        await state.update_data({
            'book_pages': pages,
            'current_reading_page': 0,
            'reading_book_id': book_id,
            'reading_book_title': title,
            'telegram_user_id': telegram_user_id,  # Сохраняем ID пользователя
            'pages_with_xp': set()  # Множество страниц за которые уже дали XP
        })

        await add_xp_for_page(telegram_user_id, 0, state)

        # Показываем первую страницу
        await show_reading_page(callback, state, bot)

    except Exception as e:
        logger.error(f"Ошибка при чтении книги: {e}")
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo,
                caption="❌ <b>Ошибка</b>\n\nНе удалось загрузить книгу.",
                parse_mode="HTML"
            ),
            reply_markup=get_book_actions_kb(book_id)
        )

    await callback.answer()


async def add_xp_for_page(telegram_user_id: int, page_number: int, state: FSMContext):
    """Добавляет XP за прочтение страницы (если еще не давали)"""
    try:
        data = await state.get_data()
        pages_with_xp = data.get('pages_with_xp', set())

        # Если за эту страницу еще не давали XP
        if page_number not in pages_with_xp:
            # Добавляем XP за страницу
            await add_xp_to_user(telegram_user_id, 5)  # +5 XP за каждую страницу

            # Обновляем статистику чтения (только для первой страницы книги)
            if page_number == 0:
                await update_user_reading_stats(telegram_user_id)

            # Добавляем страницу в множество обработанных
            pages_with_xp.add(page_number)
            await state.update_data(pages_with_xp=pages_with_xp)

            logger.info(f"Добавлено 5 XP пользователю {telegram_user_id} за страницу {page_number}")
            return True
        return False

    except Exception as e:
        logger.error(f"Ошибка при добавлении XP за страницу: {e}")
        return False


async def show_reading_page(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Показать страницу книги"""
    data = await state.get_data()
    pages = data.get('book_pages', [])
    current_page = data.get('current_reading_page', 0)
    book_id = data.get('reading_book_id')
    title = data.get('reading_book_title', 'Книга')
    telegram_user_id = data.get('telegram_user_id')
    pages_with_xp = data.get('pages_with_xp', set())

    if not pages or current_page >= len(pages):
        await callback.message.answer(
            text="❌ <b>Ошибка</b>\n\nСтраница не найдена.",
            reply_markup=get_book_actions_kb(book_id),
            parse_mode="HTML"
        )
        return

    page_content = pages[current_page]

    # Добавляем XP за текущую страницу (если еще не давали)
    xp_added = await add_xp_for_page(telegram_user_id, current_page, state)

    # Считаем общее количество полученного XP
    total_xp_earned = len(pages_with_xp) * 5

    # Формируем текст с сообщением о XP
    xp_message = "🎉 +5 XP за страницу!\n\n" if xp_added else ""

    text = f"📖 <b>{title}</b>\n\n{xp_message}{page_content}\n\n📄 Страница {current_page + 1}/{len(pages)}"

    # Для первой страницы отправляем новое сообщение, для остальных редактируем существующее
    if current_page == 0:
        await callback.message.delete()
        await callback.message.answer(
            text=text,
            reply_markup=get_reading_pagination_kb(book_id, current_page, len(pages), total_xp_earned),
            parse_mode="HTML"
        )
    else:
        try:
            await callback.message.edit_text(
                text=text,
                reply_markup=get_reading_pagination_kb(book_id, current_page, len(pages), total_xp_earned),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Ошибка при редактировании сообщения: {e}")
            # Если не удалось отредактировать, отправляем новое
            await callback.message.delete()
            await callback.message.answer(
                text=text,
                reply_markup=get_reading_pagination_kb(book_id, current_page, len(pages), total_xp_earned),
                parse_mode="HTML"
            )

@user_books_router.callback_query(F.data.startswith("read_page_"))
async def handle_reading_pagination(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Обработка пагинации при чтении книги"""
    try:
        _, _, book_id, page = callback.data.split("_")
        book_id = int(book_id)
        page = int(page)

        await state.update_data(current_reading_page=page)
        await show_reading_page(callback, state, bot)

    except Exception as e:
        logger.error(f"Ошибка при переключении страницы: {e}")
        await callback.answer("❌ Ошибка переключения страницы")

    await callback.answer()

@user_books_router.callback_query(F.data == "current_reading_page")
async def handle_current_reading_page(callback: types.CallbackQuery):
    await callback.answer("📄 Текущая страница")