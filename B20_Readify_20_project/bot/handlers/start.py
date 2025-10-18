from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from keyboards.inline_keyboards import main_menu_kb, return_menu_kb
from api.telegramusers import create_or_update_telegram_user
from aiogram.filters import Command

start_router = Router()
# photo = "AgACAgIAAxkBAAIBXmjyji-cVZO1zhue4OhyMYaTX9UtAAIL-DEbw-l5S3ATNiEmk1T9AQADAgADeQADNgQ"
photo = "AgACAgIAAxkBAAMDaPKvyEnH5FIT0qqDz0MDw7bDd3EAAgv4MRvD6XlLxL9qsd2EDbkBAAMCAAN5AAM2BA"

WELCOME_TEXT = """
👋 Привет! Добро пожаловать в Readify 1.0 — твой персональный помощник в мире книг!

📖 Читай книги прямо в Telegram
⚡ Получай XP и повышай уровень
🔥 Следи за серией дней подряд
🏆 Соревнуйся с друзьями в топе читателей
📚 Добавляй свои книги и создавай личную библиотеку

✨ Чтение стало увлекательным и мотивирующим! 
Начни свой путь к званию Легенда чтения прямо сейчас!
"""

ABOUT_BOT_TEXT = """
ℹ️ Readify 1.0 — бот для чтения и мотивации!

📚 Ты можешь:
- Читать книги прямо в Telegram
- Отслеживать прогресс и получать XP
- Соревноваться с друзьями
- Добавлять свои книги

👨‍💻 Создатели:
- Islam Duishobaev (@islam_duishobaev)
- Asanov Artyk Nuradinovich 
- Bekbolotov Yryskeldi (@Yryskeldi193)

🚀 Мы постоянно развиваемся! Следи за обновлениями!
"""

SOON_UPDATE_TEXT = """
🚀 Скоро: Readify 2.0!

Мы готовим новые фишки:
- ✨ Улучшенный интерфейс и поиск книг
- 📚 Добавление книг на русском и других языках
- 🎧 Прослушивание аудиокниг
- 📖 Ещё больше книг и жанров
- 🏆 Новые способы мотивации и наград

Следи за обновлениями и будь первым, кто попробует Readify 2.0!
"""


@start_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await create_or_update_telegram_user(message.from_user.id, message.from_user.username)
    await message.answer_photo(photo=photo, caption=WELCOME_TEXT, reply_markup=main_menu_kb())

@start_router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    try:
        await callback.message.edit_caption(caption=WELCOME_TEXT, reply_markup=main_menu_kb())
    except:
        await callback.message.answer_photo(photo=photo, caption=WELCOME_TEXT, reply_markup=main_menu_kb())

@start_router.callback_query(F.data == "about_bot")
async def about_bot(callback: CallbackQuery):
    await callback.message.edit_caption(caption=ABOUT_BOT_TEXT, reply_markup=return_menu_kb())

@start_router.callback_query(F.data == "soon_update")
async def soon_update(callback: CallbackQuery):
    await callback.message.edit_caption(caption=SOON_UPDATE_TEXT, reply_markup=return_menu_kb())

