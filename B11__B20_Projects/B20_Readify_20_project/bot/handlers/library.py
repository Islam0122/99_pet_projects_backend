from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.books import fetch_books, fetch_book_chapters, fetch_chapter
import logging
from api.telegramusers import get_telegram_user, update_user_reading_stats, add_xp_to_user

library_router = Router()
logger = logging.getLogger(__name__)

photo = "AgACAgIAAxkBAAIBXmjyji-cVZO1zhue4OhyMYaTX9UtAAIL-DEbw-l5S3ATNiEmk1T9AQADAgADeQADNgQ"


async def add_xp_for_reading(tg_id: int, chapter_length: int) -> bool:
    base_xp = max(5, min(50, chapter_length // 500))
    completion_bonus = 10
    total_xp = base_xp + completion_bonus
    result = await add_xp_to_user(tg_id, total_xp)
    return result is not None


def get_library_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Поиск книг", callback_data="search_books")],
            [InlineKeyboardButton(text="📖 Мои книги", callback_data="users_books")],
            [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
        ]
    )


def get_books_pagination_kb(books, page=0, books_per_page=5):
    start_idx = page * books_per_page
    end_idx = start_idx + books_per_page
    current_books = books[start_idx:end_idx]

    keyboard = []

    for book in current_books:
        keyboard.append([
            InlineKeyboardButton(
                text=f"📘 {book['title']}",
                callback_data=f"book_info_{book['id']}"
            )
        ])

    pagination_buttons = []

    if page > 0:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"library_page_{page - 1}"))

    total_pages = (len(books) + books_per_page - 1) // books_per_page
    if total_pages > 1:
        pagination_buttons.append(InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="current_library_page"
        ))

    if end_idx < len(books):
        pagination_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"library_page_{page + 1}"))

    if pagination_buttons:
        keyboard.append(pagination_buttons)

    keyboard.extend([
        [InlineKeyboardButton(text="🔍 Поиск книг", callback_data="search_books")],
        [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_book_actions_kb(book_id: int, total_chapters: int, current_chapter: int = 1):
    keyboard = []

    chapter_buttons = []

    if current_chapter > 1:
        chapter_buttons.append(InlineKeyboardButton(
            text="⬅️ Предыдущая",
            callback_data=f"book_chapter_{book_id}_{current_chapter - 1}"
        ))

    chapter_buttons.append(InlineKeyboardButton(
        text=f"Глава {current_chapter}/{total_chapters}",
        callback_data="current_chapter"
    ))

    if current_chapter < total_chapters:
        chapter_buttons.append(InlineKeyboardButton(
            text="Следующая ➡️",
            callback_data=f"book_chapter_{book_id}_{current_chapter + 1}"
        ))

    keyboard.append(chapter_buttons)

    keyboard.extend([
        [InlineKeyboardButton(text="📖 Начать чтение", callback_data=f"library_read_book_{book_id}_1")],
        [InlineKeyboardButton(text="📋 Список глав", callback_data=f"book_chapters_{book_id}")],
        [InlineKeyboardButton(text="📚 Назад к библиотеке", callback_data="library")],
        [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_chapters_list_kb(book_id: int, chapters, page=0, chapters_per_page=10):
    start_idx = page * chapters_per_page
    end_idx = start_idx + chapters_per_page
    current_chapters = chapters[start_idx:end_idx]

    keyboard = []

    for chapter in current_chapters:
        keyboard.append([
            InlineKeyboardButton(
                text=f"📖 {chapter['number']}. {chapter['title']}",
                callback_data=f"library_read_book_{book_id}_{chapter['number']}"
            )
        ])

    pagination_buttons = []

    if page > 0:
        pagination_buttons.append(InlineKeyboardButton(
            text="⬅️",
            callback_data=f"chapters_page_{book_id}_{page - 1}"
        ))

    total_pages = (len(chapters) + chapters_per_page - 1) // chapters_per_page
    if total_pages > 1:
        pagination_buttons.append(InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="current_chapters_page"
        ))

    if end_idx < len(chapters):
        pagination_buttons.append(InlineKeyboardButton(
            text="➡️",
            callback_data=f"chapters_page_{book_id}_{page + 1}"
        ))

    if pagination_buttons:
        keyboard.append(pagination_buttons)

    keyboard.extend([
        [InlineKeyboardButton(text="📘 О книге", callback_data=f"book_info_{book_id}")],
        [InlineKeyboardButton(text="📚 Библиотека", callback_data="library")],
        [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_text_pagination_kb(book_id: int, chapter_number: int, total_chapters: int, total_text_pages: int,
                           current_page: int = 0, xp_added: bool = False):
    keyboard = []
    pagination_buttons = []

    if current_page > 0:
        pagination_buttons.append(InlineKeyboardButton(
            text="⬅️ Предыдущая страница",
            callback_data=f"text_page_{book_id}_{chapter_number}_{current_page - 1}"
        ))

    if total_text_pages > 1:
        pagination_buttons.append(InlineKeyboardButton(
            text=f"Страница {current_page + 1}/{total_text_pages}",
            callback_data="current_text_page"
        ))

    if current_page < total_text_pages - 1:
        pagination_buttons.append(InlineKeyboardButton(
            text="Следующая страница ➡️",
            callback_data=f"text_page_{book_id}_{chapter_number}_{current_page + 1}"
        ))

    if pagination_buttons:
        keyboard.append(pagination_buttons)

    chapter_nav_buttons = []

    if chapter_number > 1:
        chapter_nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Предыдущая глава",
            callback_data=f"book_chapter_{book_id}_{chapter_number - 1}"
        ))

    chapter_nav_buttons.append(InlineKeyboardButton(
        text="📋 Список глав",
        callback_data=f"book_chapters_{book_id}"
    ))

    if chapter_number < total_chapters:
        chapter_nav_buttons.append(InlineKeyboardButton(
            text="Следующая глава ➡️",
            callback_data=f"book_chapter_{book_id}_{chapter_number + 1}"
        ))

    if chapter_nav_buttons:
        keyboard.append(chapter_nav_buttons)

    keyboard.extend([
        [InlineKeyboardButton(text="📘 О книге", callback_data=f"book_info_{book_id}")],
        [InlineKeyboardButton(text="📚 Библиотека", callback_data="library")],
        [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def split_text(text, max_length=3500):
    paragraphs = text.split('\n')
    pages = []
    current_page = ""

    for paragraph in paragraphs:
        if len(current_page) + len(paragraph) + 1 <= max_length:
            if current_page:
                current_page += '\n' + paragraph
            else:
                current_page = paragraph
        else:
            if current_page:
                pages.append(current_page)

            if len(paragraph) > max_length:
                words = paragraph.split(' ')
                current_page = ""

                for word in words:
                    if len(current_page) + len(word) + 1 <= max_length:
                        if current_page:
                            current_page += ' ' + word
                        else:
                            current_page = word
                    else:
                        pages.append(current_page)
                        current_page = word
            else:
                current_page = paragraph

    if current_page:
        pages.append(current_page)

    return pages


@library_router.callback_query(F.data == "library")
async def show_library(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await state.clear()

    try:
        books = await fetch_books()

        if not books:
            await callback.message.edit_media(
                media=types.InputMediaPhoto(
                    media=photo,
                    caption=(
                        "📚 <b>Библиотека</b>\n\n"
                        "📭 В библиотеке пока нет книг.\n\n"
                        "Книги будут добавлены в ближайшее время!"
                    ),
                    parse_mode="HTML"
                ),
                reply_markup=get_library_kb()
            )
        else:
            await state.update_data(all_books=books, current_page=0)
            await show_library_page(callback, state, bot)

    except Exception as e:
        logger.error(f"Ошибка при загрузке библиотеки: {e}")
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo,
                caption=(
                    "❌ <b>Ошибка</b>\n\n"
                    "Не удалось загрузить библиотеку. Попробуйте позже."
                ),
                parse_mode="HTML"
            ),
            reply_markup=get_library_kb()
        )

    await callback.answer()


async def show_library_page(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    books = data.get('all_books', [])
    current_page = data.get('current_page', 0)
    books_per_page = 5

    total_pages = (len(books) + books_per_page - 1) // books_per_page

    if current_page >= total_pages:
        current_page = total_pages - 1
    if current_page < 0:
        current_page = 0

    await state.update_data(current_page=current_page)

    start_idx = current_page * books_per_page
    end_idx = start_idx + books_per_page
    current_books = books[start_idx:end_idx]

    library_text = f"📚 <b>Библиотека</b> (стр. {current_page + 1}/{total_pages})\n\n"

    if not current_books:
        library_text += "📭 На этой странице нет книг."

    library_text += f"📚 Всего книг: {len(books)}"

    try:
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo,
                caption=library_text,
                parse_mode="HTML"
            ),
            reply_markup=get_books_pagination_kb(books, current_page, books_per_page)
        )
    except Exception as e:
        logger.error(f"Ошибка при редактировании библиотеки: {e}")
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=photo,
            caption=library_text,
            reply_markup=get_books_pagination_kb(books, current_page, books_per_page),
            parse_mode="HTML"
        )


@library_router.callback_query(F.data.startswith("library_page_"))
async def handle_library_pagination(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    page = int(callback.data.split("_")[2])
    await state.update_data(current_page=page)
    await show_library_page(callback, state, bot)
    await callback.answer()


@library_router.callback_query(F.data.startswith("book_info_"))
async def show_book_info(callback: types.CallbackQuery, state: FSMContext):
    book_id = int(callback.data.split("_")[2])

    try:
        books = await fetch_books()
        book = next((b for b in books if b['id'] == book_id), None)

        if not book:
            await callback.answer("❌ Книга не найдена")
            return

        book_info = (
            f"📘 <b>{book['title']}</b>\n\n"
            f"👤 <b>Автор:</b> {book['author']}\n"
            f"📖 <b>Количество глав:</b> {book['total_chapters']}\n\n"
            f"Выберите действие для чтения книги:"
        )

        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=photo,
                caption=book_info,
                parse_mode="HTML"
            ),
            reply_markup=get_book_actions_kb(book_id, book['total_chapters'])
        )

    except Exception as e:
        logger.error(f"Ошибка при показе информации о книге: {e}")
        await callback.answer("❌ Ошибка при загрузке книги")

    await callback.answer()


@library_router.callback_query(F.data.startswith("book_chapters_"))
async def show_book_chapters(callback: types.CallbackQuery, state: FSMContext):
    book_id = int(callback.data.split("_")[2])

    try:
        chapters = await fetch_book_chapters(book_id)

        if not chapters:
            await callback.answer("❌ Главы не найдены")
            return

        await state.update_data(book_chapters=chapters, book_id=book_id, chapters_page=0)
        await show_chapters_page(callback, state)

    except Exception as e:
        logger.error(f"Ошибка при загрузке глав книги: {e}")
        await callback.answer("❌ Ошибка при загрузке глав")

    await callback.answer()


async def show_chapters_page(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chapters = data.get('book_chapters', [])
    book_id = data.get('book_id')
    current_page = data.get('chapters_page', 0)
    chapters_per_page = 10

    total_pages = (len(chapters) + chapters_per_page - 1) // chapters_per_page

    if current_page >= total_pages:
        current_page = total_pages - 1
    if current_page < 0:
        current_page = 0

    await state.update_data(chapters_page=current_page)

    start_idx = current_page * chapters_per_page
    end_idx = start_idx + chapters_per_page
    current_chapters = chapters[start_idx:end_idx]

    books = await fetch_books()
    book = next((b for b in books if b['id'] == book_id), None)
    book_title = book['title'] if book else "Книга"

    chapters_text = f"📖 <b>{book_title}</b> - Список глав\n\n"

    await callback.message.edit_media(
        media=types.InputMediaPhoto(
            media=photo,
            caption=chapters_text,
            parse_mode="HTML"
        ),
        reply_markup=get_chapters_list_kb(book_id, chapters, current_page, chapters_per_page)
    )


@library_router.callback_query(F.data.startswith("chapters_page_"))
async def handle_chapters_pagination(callback: types.CallbackQuery, state: FSMContext):
    try:
        _, _, book_id, page = callback.data.split("_")
        book_id = int(book_id)
        page = int(page)

        await state.update_data(chapters_page=page)
        await show_chapters_page(callback, state)

    except Exception as e:
        logger.error(f"Ошибка при переключении страницы глав: {e}")
        await callback.answer("❌ Ошибка переключения")

    await callback.answer()


@library_router.callback_query(F.data.startswith("library_read_book_"))
async def read_library_book_chapter(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    try:
        _, _, _, book_id, chapter_number = callback.data.split("_")
        book_id = int(book_id)
        chapter_number = int(chapter_number)

        chapter = await fetch_chapter(book_id, chapter_number)

        if not chapter:
            await callback.answer("❌ Глава не найдена")
            return

        books = await fetch_books()
        book = next((b for b in books if b['id'] == book_id), None)
        if not book:
            await callback.answer("❌ Книга не найдена")
            return

        book_title = book['title']
        total_chapters = book['total_chapters']

        text_pages = split_text(chapter['text'])
        total_text_pages = len(text_pages)

        await state.update_data(
            book_id=book_id,
            chapter_number=chapter_number,
            text_pages=text_pages,
            current_text_page=0,
            total_text_pages=total_text_pages,
            total_chapters=total_chapters,
            xp_added=False
        )

        chapter_text = (
            f"📘 <b>{book_title}</b>\n"
            f"📖 <b>Глава {chapter['number']}: {chapter['title']}</b>\n\n"
            f"{text_pages[0]}"
        )

        if total_text_pages > 1:
            chapter_text += f"\n\n📄 Страница 1/{total_text_pages}"

        await callback.message.answer(
            text=chapter_text,
            reply_markup=get_text_pagination_kb(book_id, chapter_number, total_chapters, total_text_pages, 0, False),
            parse_mode="HTML"
        )

    except Exception as e:
        logger.error(f"Ошибка при чтении главы из библиотеки: {e}")
        await callback.answer("❌ Ошибка при загрузке главы")

    await callback.answer()


@library_router.callback_query(F.data.startswith("book_chapter_"))
async def navigate_book_chapter(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    try:
        _, _, book_id, chapter_number = callback.data.split("_")
        book_id = int(book_id)
        chapter_number = int(chapter_number)

        chapter = await fetch_chapter(book_id, chapter_number)

        if not chapter:
            await callback.answer("❌ Глава не найдена")
            return

        books = await fetch_books()
        book = next((b for b in books if b['id'] == book_id), None)
        if not book:
            await callback.answer("❌ Книга не найдена")
            return

        book_title = book['title']
        total_chapters = book['total_chapters']

        text_pages = split_text(chapter['text'])
        total_text_pages = len(text_pages)

        await state.update_data(
            book_id=book_id,
            chapter_number=chapter_number,
            text_pages=text_pages,
            current_text_page=0,
            total_text_pages=total_text_pages,
            total_chapters=total_chapters,
            xp_added=False
        )

        chapter_text = (
            f"📘 <b>{book_title}</b>\n"
            f"📖 <b>Глава {chapter['number']}: {chapter['title']}</b>\n\n"
            f"{text_pages[0]}"
        )

        if total_text_pages > 1:
            chapter_text += f"\n\n📄 Страница 1/{total_text_pages}"

        if callback.message.content_type == 'text':
            await callback.message.edit_text(
                text=chapter_text,
                reply_markup=get_text_pagination_kb(book_id, chapter_number, total_chapters, total_text_pages, 0,
                                                    False),
                parse_mode="HTML"
            )
        else:
            await callback.message.answer(
                text=chapter_text,
                reply_markup=get_text_pagination_kb(book_id, chapter_number, total_chapters, total_text_pages, 0,
                                                    False),
                parse_mode="HTML"
            )

    except Exception as e:
        logger.error(f"Ошибка при навигации по главам библиотеки: {e}")
        await callback.answer("❌ Ошибка при загрузке главы")

    await callback.answer()


@library_router.callback_query(F.data.startswith("text_page_"))
async def navigate_text_page(callback: types.CallbackQuery, state: FSMContext):
    try:
        _, _, book_id, chapter_number, page = callback.data.split("_")
        book_id = int(book_id)
        chapter_number = int(chapter_number)
        page = int(page)

        data = await state.get_data()
        text_pages = data.get('text_pages', [])
        total_text_pages = data.get('total_text_pages', 1)
        total_chapters = data.get('total_chapters', 1)
        xp_added = data.get('xp_added', False)

        if page < 0 or page >= total_text_pages:
            await callback.answer("❌ Страница не найдена")
            return

        books = await fetch_books()
        book = next((b for b in books if b['id'] == book_id), None)
        book_title = book['title'] if book else "Книга"

        chapter = await fetch_chapter(book_id, chapter_number)
        if not chapter:
            await callback.answer("❌ Глава не найдена")
            return

        chapter_text = (
            f"📘 <b>{book_title}</b>\n"
            f"📖 <b>Глава {chapter['number']}: {chapter['title']}</b>\n\n"
            f"{text_pages[page]}"
        )

        if total_text_pages > 1:
            chapter_text += f"\n\n📄 Страница {page + 1}/{total_text_pages}"

        if page == total_text_pages - 1 and not xp_added:
            tg_id = callback.from_user.id
            success = await add_xp_for_reading(tg_id, len(chapter['text']))

            if success:
                await state.update_data(xp_added=True)
                chapter_text += "\n\n🎯 <b>+XP!</b>"
                xp_added = True
                await callback.answer("🎯 XP  начислены!")
            else:
                chapter_text += "\n\n❌ <b>Не удалось начислить XP</b>"
                await callback.answer("❌ Ошибка при начислении XP")

        await state.update_data(current_text_page=page)

        await callback.message.edit_text(
            text=chapter_text,
            reply_markup=get_text_pagination_kb(book_id, chapter_number, total_chapters, total_text_pages, page,
                                                xp_added),
            parse_mode="HTML"
        )

    except Exception as e:
        logger.error(f"Ошибка при навигации по страницам текста: {e}")
        await callback.answer("❌ Ошибка при загрузке страницы")

    await callback.answer()


@library_router.callback_query(F.data == "refresh_library")
async def refresh_library(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await show_library(callback, state, bot)
    await callback.answer("🔄 Библиотека обновлена")


@library_router.callback_query(F.data == "current_library_page")
async def handle_current_library_page(callback: types.CallbackQuery):
    await callback.answer("📄 Текущая страница библиотеки")


@library_router.callback_query(F.data == "current_chapter")
async def handle_current_chapter(callback: types.CallbackQuery):
    await callback.answer("📖 Текущая глава")


@library_router.callback_query(F.data == "current_chapters_page")
async def handle_current_chapters_page(callback: types.CallbackQuery):
    await callback.answer("📄 Текущая страница глав")


@library_router.callback_query(F.data == "current_text_page")
async def handle_current_text_page(callback: types.CallbackQuery):
    await callback.answer("📄 Текущая страница текста")