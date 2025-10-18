from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.books import fetch_user_books, delete_user_book, read_user_book
from api.telegramusers import get_telegram_user
import logging

user_books_router = Router()
logger = logging.getLogger(__name__)
photo = "AgACAgIAAxkBAAIBXmjyji-cVZO1zhue4OhyMYaTX9UtAAIL-DEbw-l5S3ATNiEmk1T9AQADAgADeQADNgQ"


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
        telegram_user_id = user_data['id']

        all_books = await fetch_user_books()

        user_books = [
            book for book in all_books
            if book.get('telegram_user') == telegram_user_id
        ]

        if not user_books:
            await callback.message.edit_caption(
                caption=(
                    "📖 <b>Мои книги</b>\n\n"
                    "📭 У вас пока нет добавленных книг.\n\n"
                    "Нажмите '📤 Добавить книгу' чтобы добавить свою первую книгу!"
                ),
                reply_markup=get_user_books_kb(),
                parse_mode="HTML"
            )
        else:
            await state.update_data(all_user_books=user_books, current_page=0)
            await show_books_page(callback, state, bot)

    except Exception as e:
        logger.error(f"Ошибка при получении книг пользователя: {e}")
        await callback.message.edit_caption(
            caption=(
                "❌ <b>Ошибка</b>\n\n"
                "Не удалось загрузить ваши книги. Попробуйте позже."
            ),
            reply_markup=get_user_books_kb(),
            parse_mode="HTML"
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
        try:
            await callback.message.edit_caption(
            caption=book_text,
            reply_markup=get_book_actions_kb(book_id),
            parse_mode="HTML"
            )
        except Exception as e:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=photo,
                caption=book_text,
                reply_markup=get_book_actions_kb(book_id),
                parse_mode="HTML"
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
            await callback.message.edit_caption(
                caption="✅ <b>Книга успешно удалена!</b>",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="📖 Мои книги", callback_data="users_books")],
                        [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
                    ]
                ),
                parse_mode="HTML"
            )
        else:
            await callback.message.edit_caption(
                caption="❌ <b>Ошибка</b>\n\nНе удалось удалить книгу.",
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="📖 Мои книги", callback_data="users_books")],
                        [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
                    ]
                ),
                parse_mode="HTML"
            )

    except Exception as e:
        logger.error(f"Ошибка при удалении книги: {e}")
        await callback.message.edit_caption(
            caption="❌ <b>Ошибка</b>\n\nНе удалось удалить книгу.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="📖 Мои книги", callback_data="users_books")],
                    [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
                ]
            ),
            parse_mode="HTML"
        )

    await callback.answer()


def get_reading_pagination_kb(book_id: int, current_page: int, total_pages: int):
    """Клавиатура для пагинации при чтении книги"""
    keyboard = []

    # Кнопки пагинации
    pagination_buttons = []

    if current_page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(text="⬅️", callback_data=f"read_page_{book_id}_{current_page - 1}"))

    pagination_buttons.append(InlineKeyboardButton(
        text=f"{current_page + 1}/{total_pages}",
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
        # for i, book in enumerate(current_books, start_idx + 1):
            # books_text += f"{i}. <b>{book['title']}</b>\n"
            # if book.get('description'):
            #     books_text += f"   📝 {book['description'][:50]}...\n"
            # books_text += f"   📅 {book['created_at'][:10]}\n\n"

    books_text += f"📚 Всего книг: {len(user_books)}"

    try:
        await callback.message.edit_caption(
            caption=books_text,
            reply_markup=get_books_pagination_kb(user_books, current_page, books_per_page),
            parse_mode="HTML"
        )
    except Exception as e:
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
    """Чтение книги с пагинацией"""
    book_id = int(callback.data.split("_")[2])

    try:
        await callback.message.edit_caption(
            caption="⏳ <b>Загружаю книгу...</b>",
            reply_markup=None,
            parse_mode="HTML"
        )

        book_content = await read_user_book(book_id)

        if not book_content:
            await callback.message.edit_caption(
                caption="❌ <b>Ошибка</b>\n\nНе удалось загрузить книгу.",
                reply_markup=get_book_actions_kb(book_id),
                parse_mode="HTML"
            )
            return

        content = book_content.get('content', '')
        title = book_content.get('title', 'Книга')

        # Разбиваем на страницы
        MAX_PAGE_LENGTH = 3000  # символов на страницу
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
            'reading_book_title': title
        })

        # Показываем первую страницу
        await show_reading_page(callback, state, bot)

    except Exception as e:
        logger.error(f"Ошибка при чтении книги: {e}")
        await callback.message.edit_caption(
            caption="❌ <b>Ошибка</b>\n\nНе удалось загрузить книгу.",
            reply_markup=get_book_actions_kb(book_id),
            parse_mode="HTML"
        )

    await callback.answer()


async def show_reading_page(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    """Показать страницу книги"""
    data = await state.get_data()
    pages = data.get('book_pages', [])
    current_page = data.get('current_reading_page', 0)
    book_id = data.get('reading_book_id')
    title = data.get('reading_book_title', 'Книга')

    if not pages or current_page >= len(pages):
        await callback.message.edit_caption(
            caption="❌ <b>Ошибка</b>\n\nСтраница не найдена.",
            reply_markup=get_book_actions_kb(book_id),
            parse_mode="HTML"
        )
        return

    page_content = pages[current_page]

    # Формируем текст
    text = f"📖 <b>{title}</b>\n\n{page_content}\n\n📄 Страница {current_page + 1}/{len(pages)}"
    await callback.message.delete()
    await callback.message.answer(
        text=text,
        reply_markup=get_reading_pagination_kb(book_id, current_page, len(pages)),
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
    """Обработка нажатия на номер текущей страницы чтения"""
    await callback.answer("📄 Текущая страница")

