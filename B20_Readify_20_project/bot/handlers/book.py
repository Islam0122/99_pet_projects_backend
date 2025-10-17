from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.books import load_book,fetch_chapter
from keyboards.inline_keyboards import return_menu_kb
from aiogram.filters import CommandObject, Command

book_router = Router()
photo = "AgACAgIAAxkBAAIBXmjyji-cVZO1zhue4OhyMYaTX9UtAAIL-DEbw-l5S3ATNiEmk1T9AQADAgADeQADNgQ"

text = "❗ Укажите название книги после команды /search\n📖 Пример: /search Гарри Поттер\n⚠️ Если книга не найдена, проверьте правильность написания названия."

@book_router.callback_query(F.data == "search_book")
async def search_book_handler(query: types.CallbackQuery):
    await query.message.edit_caption(caption=text, reply_markup=return_menu_kb())


@book_router.message(Command(commands=["search"]))
async def search_book(message: types.Message, command: CommandObject):
    book_name = command.args
    if not book_name:
        await message.answer(
            text
        )
        return

    book_data = await load_book(book_name)
    if not book_data:
        await message.answer(
            "📚 Книг с таким названием не найдено.", reply_markup=return_menu_kb()
        )
        return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Читать", callback_data=f"chapter_{book_data['id']}")],
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu")]
    ])

    await message.answer(
        f"📚 Найдена книга: {book_data['title']} — {book_data['author']}",
        reply_markup=kb
    )

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

PAGE_SIZE = 1000  # кол-во символов на одну страницу

def chapter_pages(text: str):
    """Разбивает текст на страницы по PAGE_SIZE символов"""
    return [text[i:i+PAGE_SIZE] for i in range(0, len(text), PAGE_SIZE)]

def make_chapter_kb(book_id: int, chapter_number: int, page: int, total_pages: int):
    kb = []
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"chapter_{book_id}_{chapter_number}_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("➡️ Вперед", callback_data=f"chapter_{book_id}_{chapter_number}_{page+1}"))
    if nav_buttons:
        kb.append(nav_buttons)
    kb.append([InlineKeyboardButton("⬅️ Назад в меню", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

# Хендлер для показа главы
@book_router.callback_query(F.data.startswith("chapter_"))
async def chapter_page_handler(query: CallbackQuery):
    _, book_id, chapter_number, page = query.data.split("_")
    book_id, chapter_number, page = int(book_id), int(chapter_number), int(page)

    chapter = await fetch_chapter(book_id, chapter_number)
    if not chapter:
        await query.message.edit_text("⚠️ Не удалось загрузить главу.", reply_markup=return_menu_kb())
        return

    pages = chapter_pages(chapter['text'])
    total_pages = len(pages)

    text = f"📖 {chapter['title']}\n\n{pages[page]}"
    kb = make_chapter_kb(book_id, chapter_number, page, total_pages)

    await query.message.edit_text(text=text, reply_markup=kb)




