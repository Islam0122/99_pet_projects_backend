from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.books import load_book
from keyboards.inline_keyboards import return_menu_kb
from aiogram.filters import CommandObject, Command

book_router = Router()
photo = "AgACAgIAAxkBAAIBXmjyji-cVZO1zhue4OhyMYaTX9UtAAIL-DEbw-l5S3ATNiEmk1T9AQADAgADeQADNgQ"

text = "❗ Укажите название книги после команды /search\n📖 Пример: /search Pride and Prejudice \n⚠️ Если книга не найдена, проверьте правильность написания названия."

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
        [InlineKeyboardButton(text="📘 О книге", callback_data=f"book_info_{book_data['id']}")],
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu")]
    ])

    await message.answer(
        f"📚 Найдена книга: {book_data['title']} — {book_data['author']}",
        reply_markup=kb
    )
