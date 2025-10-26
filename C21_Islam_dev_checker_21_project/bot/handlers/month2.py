from aiogram import Router, types, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from external_services.api_client_user import StudentAPI, GroupsAPI
from keyboards.inline_keyboards import get_main_menu, get_teacher_account, return_menu
import logging
import re
from aiogram import types
from datetime import datetime
from aiogram import Router, types, Bot, F
from aiogram.fsm.context import FSMContext
from external_services.api_client_user import StudentAPI, HWMonth2 as HWMonth3
from keyboards.inline_keyboards import get_main_menu
import logging

month2_router = Router()
photo = types.FSInputFile("img.png")

TASK_2_MONTH_LESSON_CHOICES = [
    ("Создание первого бота", "📱 Урок 1: Настройка токена и создание первого бота"),
    ("Обработка сообщений и команд", "💬 Урок 2: Основы обработки сообщений и команд"),
    ("Кнопки (Reply и Inline)", "⌨️ Урок 3: Добавление кнопок Reply и Inline"),
    ("FSM: состояния и хранение данных", "🔄 Урок 4: Состояния и хранение данных"),
    ("Практика: бот-анкета", "📝 Урок 5: Практическая работа — бот анкета"),
    ("Подключение базы данных (SQLite)", "💾 Урок 6: Подключение базы данных"),
    ("CRUD-операции в БД", "🗃️ Урок 7: Создание, чтение, обновление, удаление"),
    ("Интеграция БД с ботом", "🔗 Урок 8: Связь бота с базой данных"),
    ("FSMAdmin, админ-панель", "👑 Урок 9: Работа с FSMAdmin и админкой"),
    ("Практика: бот-магазин (без оплаты)", "🛒 Урок 10: Практика — магазин бот"),
    ("Работа с API (requests)", "🌐 Урок 11: Использование API"),
    ("Web scraping (BS4)", "🕸️ Урок 12: Сбор данных с веб-сайтов"),
    ("Планировщик задач (Aioschedule)", "⏰ Урок 13: Настройка планировщика задач"),
    ("Middleware, фильтры, флаги", "⚙️ Урок 14: Настройка Middleware и фильтров"),
    ("Практика: бот-новостник или бот-напоминалка", "📰 Урок 15: Практическая работа"),
    ("Git/GitHub --> command", "🔧 Урок 16: Основы Git"),
    ("Git/GitHub / Деплой на сервер (Heroku/VPS)", "🚀 Урок 17: Деплой проекта"),
    ("Практика: деплой Telegram-бота", "🌍 Урок 18: Практическая работа"),
    ("Итоговый проект месяца (командная работа)", "👥 Урок 19: Командная работа"),
    ("Презентация проектов", "🎤 Урок 20: Презентация результатов"),
]


class Homework2States(StatesGroup):
    waiting_for_lesson = State()
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_github_url = State()


user_last_message = {}


@month2_router.callback_query(F.data == "cancel")
async def cancel_task_3month(callback: types.CallbackQuery, state: FSMContext):
    """Отмена создания домашнего задания"""
    user_id = callback.from_user.id
    if user_id in user_last_message:
        try:
            await callback.bot.edit_message_caption(
                chat_id=callback.message.chat.id,
                message_id=user_last_message[user_id],
                caption="❌ *Создание домашнего задания отменено*\n\n"
                        "Вы можете вернуться к созданию задания в любое время через главное меню 👇",
                reply_markup=get_main_menu(),
                parse_mode="Markdown"
            )
        except Exception:
            await callback.message.answer(
                "❌ Создание домашнего задания отменено",
                reply_markup=get_main_menu()
            )
    else:
        await callback.message.answer(
            "❌ Создание домашнего задания отменено",
            reply_markup=get_main_menu()
        )

    await state.clear()
    await callback.answer()


@month2_router.callback_query(F.data == "month:2")
async def send_task_3month(callback: types.CallbackQuery):
    """Главное меню 3-го месяца"""
    user_id = callback.from_user.id

    try:
        await callback.message.edit_caption(
            caption="🎯 *2-й месяц: Aiogram*\n\n"
                    "📚 *Выберите урок для отправки домашнего задания:*\n"
                    "────────────────────",
            reply_markup=generate_lessons_keyboard(),
            parse_mode="Markdown"
        )
        user_last_message[user_id] = callback.message.message_id
    except Exception:
        new_message = await callback.message.answer_photo(
            photo=photo,
            caption="🎯 *2-й месяц: Aiogram*\n\n"
                    "📚 *Выберите урок для отправки домашнего задания:*\n"
                    "────────────────────",
            reply_markup=generate_lessons_keyboard(),
            parse_mode="Markdown"
        )
        user_last_message[user_id] = new_message.message_id

    await callback.answer()


@month2_router.callback_query(F.data.startswith("lesson2_"))
async def select_lesson(callback: types.CallbackQuery, state: FSMContext):
    """Выбор урока для домашнего задания"""
    user_id = callback.from_user.id
    lesson_number = callback.data.split("_")[1]
    lesson_name = get_lesson_name_by_number(lesson_number)
    lesson_display = get_lesson_display_name(lesson_name)

    await state.update_data(lesson=lesson_name, lesson_display=lesson_display)

    try:
        await callback.message.edit_caption(
            caption=f"✅ *Выбран урок:* {lesson_display}\n\n"
                    "📝 *Введите название вашего домашнего задания:*\n"
                    "────────────────────\n",
            reply_markup=get_cancel_keyboard(),
            parse_mode="Markdown"
        )
        user_last_message[user_id] = callback.message.message_id
    except Exception as e:
        logging.error(f"Error editing message: {e}")
        new_message = await callback.message.answer_photo(
            photo=photo,
            caption=f"✅ *Выбран урок:* {lesson_display}\n\n"
                    "📝 *Введите название вашего домашнего задания:*\n"
                    ,
            reply_markup=get_cancel_keyboard(),
            parse_mode="Markdown"
        )
        user_last_message[user_id] = new_message.message_id

    await state.set_state(Homework2States.waiting_for_title)
    await callback.answer()


@month2_router.message(Homework2States.waiting_for_title)
async def process_title(message: types.Message, state: FSMContext):
    """Обработка названия домашнего задания"""
    user_id = message.from_user.id
    title = message.text.strip()

    await state.update_data(title=title)

    data = await state.get_data()
    lesson_display = data.get('lesson_display', '')

    try:
        await message.bot.edit_message_caption(
            chat_id=message.chat.id,
            message_id=user_last_message.get(user_id),
            caption=f"✅ *Урок:* {lesson_display}\n"
                    f"📝 *Название:* {title}\n\n"
                    "📋 *Опишите условие задания или что вы сделали:*\n"
                    ,
            reply_markup=get_cancel_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Error editing message: {e}")
        new_message = await message.answer_photo(
            photo=photo,
            caption=f"✅ *Урок:* {lesson_display}\n"
                    f"📝 *Название:* {title}\n\n"
                    "📋 *Опишите условие задания или что вы сделали:*\n"
                    ,
            reply_markup=get_cancel_keyboard(),
            parse_mode="Markdown"
        )
        user_last_message[user_id] = new_message.message_id

    await state.set_state(Homework2States.waiting_for_description)
    await message.delete()


@month2_router.message(Homework2States.waiting_for_description)
async def process_description(message: types.Message, state: FSMContext):
    """Обработка описания домашнего задания"""
    user_id = message.from_user.id
    description = message.text.strip()

    await state.update_data(description=description)

    data = await state.get_data()
    lesson_display = data.get('lesson_display', '')
    title = data.get('title', '')

    try:
        await message.bot.edit_message_caption(
            chat_id=message.chat.id,
            message_id=user_last_message.get(user_id),
            caption=f"✅ *Урок:* {lesson_display}\n"
                    f"📝 *Название:* {title}\n"
                    f"📋 *Описание:* {description[:50]}...\n\n"
                    "🔗 *ОБЯЗАТЕЛЬНО пришлите ссылку на GitHub репозиторий:*\n"
                    "────────────────────\n"
                    "📌 *GitHub ссылка обязательна для проверки!*\n"
                    "💡 *Формат:* https://github.com/username/repository\n\n"
                    "*Примеры:*\n"
                    "• https://github.com/ivanov/django-blog\n"
                    "• https://github.com/petrov/python-shop",
            reply_markup=get_cancel_keyboard(),
            parse_mode="Markdown"
        )
    except Exception as e:
        logging.error(f"Error editing message: {e}")
        new_message = await message.answer_photo(
            photo=photo,
            caption=f"✅ *Урок:* {lesson_display}\n"
                    f"📝 *Название:* {title}\n"
                    f"📋 *Описание:* {description[:50]}...\n\n"
                    "🔗 *ОБЯЗАТЕЛЬНО пришлите ссылку на GitHub репозиторий:*\n"
                    "────────────────────\n"
                    "📌 *GitHub ссылка обязательна для проверки!*\n"
                    "💡 *Формат:* https://github.com/username/repository\n\n"
                    "*Примеры:*\n"
                    "• https://github.com/ivanov/django-blog\n"
                    "• https://github.com/petrov/python-shop",
            reply_markup=get_cancel_keyboard(),
            parse_mode="Markdown"
        )
        user_last_message[user_id] = new_message.message_id

    await state.set_state(Homework2States.waiting_for_github_url)
    await message.delete()


@month2_router.message(Homework2States.waiting_for_github_url)
async def process_github_url(message: types.Message, state: FSMContext, bot: Bot):
    """Обработка GitHub ссылки и создание домашнего задания"""
    user_id = message.from_user.id

    try:
        github_url = message.text.strip()

        # Проверяем, что пользователь не пытается пропустить
        if github_url.lower() in ['нет', 'no', 'skip', '-', '']:
            try:
                await message.bot.edit_message_caption(
                    chat_id=message.chat.id,
                    message_id=user_last_message.get(user_id),
                    caption=(
                        "❌ *GitHub ссылка ОБЯЗАТЕЛЬНА!*\n\n"
                        "🔗 *Пришлите ссылку на GitHub репозиторий:*\n"
                        "────────────────────\n"
                        "📌 *Без GitHub репозитория задание не может быть принято!*\n\n"
                        "*Правильный формат:*\n"
                        "• https://github.com/username/repository-name\n\n"
                        "*Пример:*\n"
                        "• https://github.com/ivanov/django-blog\n"
                        "• https://github.com/petrov/python-shop"
                    ),
                    reply_markup=get_cancel_keyboard(),
                    parse_mode="Markdown"
                )
                await message.delete()
            except Exception as e:
                if "message is not modified" not in str(e):
                    logging.error(f"Error editing message: {e}")
                    new_message = await message.answer_photo(
                        photo=photo,
                        caption=(
                            "❌ *GitHub ссылка ОБЯЗАТЕЛЬНА!*\n\n"
                            "🔗 *Пришлите ссылку на GitHub репозиторий:*\n"
                            "────────────────────\n"
                            "📌 *Без GitHub репозитория задание не может быть принято!*\n\n"
                            "*Правильный формат:*\n"
                            "• https://github.com/username/repository-name\n\n"
                            "*Пример:*\n"
                            "• https://github.com/ivanov/django-blog\n"
                            "• https://github.com/petrov/python-shop"
                        ),
                        reply_markup=get_cancel_keyboard(),
                        parse_mode="Markdown"
                    )
                    user_last_message[user_id] = new_message.message_id
                    await message.delete()
            return

        # Проверяем валидность GitHub URL
        if not is_valid_github_url(github_url):
            try:
                await message.bot.edit_message_caption(
                    chat_id=message.chat.id,
                    message_id=user_last_message.get(user_id),
                    caption=(
                        "❌ *Неверный формат GitHub ссылки!*\n\n"
                        "🔗 *Пришлите ссылку в правильном формате:*\n"
                        "────────────────────\n"
                        "*Правильный формат:*\n"
                        "• https://github.com/username/repository-name\n\n"
                        "*Примеры:*\n"
                        "• https://github.com/ivanov/django-blog\n"
                        "• https://github.com/petrov/python-shop\n\n"
                        "❌ *Неправильно:*\n"
                        "• github.com/username (без https://)\n"
                        "• https://github.com/username (без названия репозитория)\n"
                        "• gitlab.com/... (только GitHub принимается)\n\n"
                        "💡 *Совет:* Скопируйте ссылку прямо из адресной строки браузера"
                    ),
                    reply_markup=get_cancel_keyboard(),
                    parse_mode="Markdown"
                )
                await message.delete()

            except Exception as e:
                if "message is not modified" not in str(e):
                    logging.error(f"Error editing message: {e}")
                    new_message = await message.answer_photo(
                        photo=photo,
                        caption=(
                            "❌ *Неверный формат GitHub ссылки!*\n\n"
                            "🔗 *Пришлите ссылку в правильном формате:*\n"
                            "────────────────────\n"
                            "*Правильный формат:*\n"
                            "• https://github.com/username/repository-name\n\n"
                            "*Примеры:*\n"
                            "• https://github.com/ivanov/django-blog\n"
                            "• https://github.com/petrov/python-shop"
                        ),
                        reply_markup=get_cancel_keyboard(),
                        parse_mode="Markdown"
                    )
                    user_last_message[user_id] = new_message.message_id
                    await message.delete()

            return

        user_data = await state.get_data()

        # Получаем информацию о студенте
        async with StudentAPI() as student_api:
            student = await student_api.get_student_by_telegram_id(str(message.from_user.id))

        if not student:
            try:
                await message.bot.edit_message_caption(
                    chat_id=message.chat.id,
                    message_id=user_last_message.get(user_id),
                    caption=(
                        "❌ *Студент не найден!*\n\n"
                        "Обратитесь к администратору для решения проблемы 👨‍💼"
                    ),
                    reply_markup=get_main_menu(),
                    parse_mode="Markdown"
                )
            except Exception as e:
                if "message is not modified" not in str(e):
                    logging.error(f"Error editing message: {e}")
                    await message.answer(
                        "❌ Студент не найден. Обратитесь к администратору.",
                        reply_markup=get_main_menu()
                    )
            await state.clear()
            return

        try:
            await message.bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=user_last_message.get(user_id),
                caption=(
                    "⏳ *Создаем домашнее задание...*\n\n"
                    "Пожалуйста, подождите немного ⏰"
                ),
                reply_markup=None,
                parse_mode="Markdown"
            )
        except Exception as e:
            if "message is not modified" not in str(e):
                logging.error(f"Error editing message: {e}")
                new_message = await message.answer_photo(
                    photo=photo,
                    caption=(
                        "⏳ *Создаем домашнее задание...*\n\n"
                        "Пожалуйста, подождите немного ⏰"
                    ),
                    reply_markup=None,
                    parse_mode="Markdown"
                )
                user_last_message[user_id] = new_message.message_id

        # Создаем домашнее задание
        async with HWMonth3() as hw_api:
            homework_data = await hw_api.create_homework(
                student_id=student['id'],
                lesson=user_data['lesson'],
                title=user_data['title'],
                task_condition=user_data['description'],
                github_url=github_url
            )

        if homework_data and "error" not in homework_data:
            lesson_display = user_data.get('lesson_display', get_lesson_display_name(user_data['lesson']))

            # Форматируем дату
            created_at = homework_data.get('created_at', '')
            if created_at:
                try:
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    created_at = dt.strftime("%d.%m.%Y в %H:%M")
                except:
                    created_at = "сегодня"

            status_icon = "✅" if homework_data.get('is_checked') else "⏳"
            status_text = "Проверено" if homework_data.get('is_checked') else "Ожидает проверки"

            success_caption = (
                f"🎉 *Домашнее задание успешно создано!*\n\n"
                f"📚 *Урок:* {lesson_display}\n"
                f"📝 *Название:* {user_data['title']}\n"
                f"🔗 *GitHub:* {github_url}\n"
                f"📅 *Отправлено:* {created_at}\n"
                f"📊 *Статус:* {status_icon} {status_text}\n\n"
                f"💫 *Желаем успехов в обучении!*"
            )

            try:
                await message.bot.edit_message_caption(
                    chat_id=message.chat.id,
                    message_id=user_last_message.get(user_id),
                    caption=success_caption,
                    reply_markup=get_main_menu(),
                    parse_mode="Markdown"
                )
            except Exception as e:
                if "message is not modified" not in str(e):
                    logging.error(f"Error editing success message: {e}")
                    # Пробуем отправить без Markdown, если есть ошибки форматирования
                    await message.answer_photo(
                        photo=photo,
                        caption=(
                            "🎉 Домашнее задание успешно создано!\n\n"
                            f"📚 Урок: {lesson_display}\n"
                            f"📝 Название: {user_data['title']}\n"
                            f"🔗 GitHub: {github_url}\n"
                            f"📅 Отправлено: {created_at}\n"
                            f"📊 Статус: {status_icon} {status_text}\n\n"
                            f"💫 Желаем успехов в обучении!"
                        ),
                        reply_markup=get_main_menu(),
                        parse_mode=None  # Отключаем Markdown
                    )

            # Очищаем состояние только при успешном создании
            await state.clear()
            try:
                await message.delete()
            except Exception:
                pass  # Игнорируем ошибки удаления сообщения

        else:
            # Обрабатываем ошибку создания (включая случай дубликата)
            error_message = homework_data.get('error', '') if homework_data else "Неизвестная ошибка"

            if "уже создали домашку" in error_message.lower():
                # Случай когда задание уже существует
                lesson_display = user_data.get('lesson_display', get_lesson_display_name(user_data['lesson']))

                duplicate_caption = (
                    f"⚠️ *Задание уже существует!*\n\n"
                    f"📚 *Урок:* {lesson_display}\n"
                    f"📝 *Название:* {user_data['title']}\n\n"
                    f"💡 *Вы уже отправляли домашнее задание по этому уроку.*\n\n"
                    f"📌 *Что можно сделать:*\n"
                    f"• Проверить свои отправленные задания\n"
                    f"• Обновить существующее задание\n"
                    f"• Выбрать другой урок"
                )

                try:
                    await message.bot.edit_message_caption(
                        chat_id=message.chat.id,
                        message_id=user_last_message.get(user_id),
                        caption=duplicate_caption,
                        reply_markup=get_duplicate_keyboard(),
                        parse_mode="Markdown"
                    )
                    await message.delete()

                except Exception as e:
                    if "message is not modified" not in str(e):
                        logging.error(f"Error editing duplicate message: {e}")
                        await message.answer_photo(
                            photo=photo,
                            caption=duplicate_caption,
                            reply_markup=get_duplicate_keyboard(),
                            parse_mode="Markdown"
                        )
                        await message.delete()

            else:
                lesson_display = user_data.get('lesson_display', get_lesson_display_name(user_data['lesson']))
                error_caption = (
                    f"⚠️ *Задание уже существует!*\n\n"
                    f"📚 *Урок:* {lesson_display}\n"
                    f"📝 *Название:* {user_data['title']}\n\n"
                    f"💡 *Вы уже отправляли домашнее задание по этому уроку.*\n\n"
                    f"📌 *Что можно сделать:*\n"
                    f"• Проверить свои отправленные задания\n"
                    f"• Обновить существующее задание\n"
                    f"• Выбрать другой урок"
                )

                try:
                    await message.bot.edit_message_caption(
                        chat_id=message.chat.id,
                        message_id=user_last_message.get(user_id),
                        caption=error_caption,
                        reply_markup=get_retry_keyboard(),
                        parse_mode="Markdown"
                    )
                    await message.delete()

                except Exception as e:
                    if "message is not modified" not in str(e):
                        logging.error(f"Error editing error message: {e}")
                        await message.answer_photo(
                            photo=photo,
                            caption=error_caption,
                            reply_markup=get_retry_keyboard(),
                            parse_mode="Markdown"
                        )
                        await message.delete()


    except Exception as e:
        logging.error(f"Unexpected error creating homework: {e}")
        try:
            await message.bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=user_last_message.get(user_id),
                caption=(
                    "❌ *Произошла непредвиденная ошибка!*\n\n"
                    "Попробуйте позже или обратитесь к администратору 👨‍💼"
                ),
                reply_markup=get_retry_keyboard(),
                parse_mode="Markdown"
            )
            await message.delete()

        except Exception as edit_error:
            if "message is not modified" not in str(edit_error):
                logging.error(f"Error editing unexpected error message: {edit_error}")
                await message.answer(
                    "❌ Произошла ошибка при создании задания. Попробуйте позже.",
                    reply_markup=get_retry_keyboard()
                )
            await message.delete()


def get_duplicate_keyboard():
    """Клавиатура для случая дубликата задания"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="🔄 Выбрать другой урок", callback_data="month:2")],
            [types.InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu")]
        ]
    )


def get_retry_keyboard():
    """Клавиатура с кнопкой повторной попытки"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="🔄 Попробовать снова", callback_data="month:2")],
            [types.InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ]
    )


def is_valid_github_url(url: str) -> bool:
    """Проверка валидности GitHub URL"""
    import re

    # Более строгая проверка
    pattern = r'^https?://(www\.)?github\.com/[a-zA-Z0-9\-_.]+/[a-zA-Z0-9\-_.]+/?$'

    if not re.match(pattern, url):
        return False

    # Дополнительные проверки
    parts = url.split('/')
    if len(parts) < 5:
        return False

    # Проверяем что username и repository-name не пустые
    username = parts[3]
    repo_name = parts[4]

    if not username or not repo_name:
        return False

    return True


def get_lesson_display_name(lesson_value: str) -> str:
    """Получить отображаемое название урока по значению"""
    for value, display in TASK_2_MONTH_LESSON_CHOICES:
        if value == lesson_value:
            return display
    return lesson_value


def generate_lessons_keyboard():
    """Генерация клавиатуры с уроками"""
    buttons = []

    for i in range(0, len(TASK_2_MONTH_LESSON_CHOICES), 2):
        row = []
        for j in range(2):
            if i + j < len(TASK_2_MONTH_LESSON_CHOICES):
                lesson_value, lesson_display = TASK_2_MONTH_LESSON_CHOICES[i + j]
                row.append(
                    types.InlineKeyboardButton(
                        text=lesson_display,
                        callback_data=f"lesson2_{i + j + 1}"
                    )
                )
        buttons.append(row)

    buttons.append([types.InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")])

    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def get_lesson_name_by_number(lesson_number: str):
    """Получить название урока по номеру"""
    try:
        index = int(lesson_number) - 1
        if 0 <= index < len(TASK_2_MONTH_LESSON_CHOICES):
            return TASK_2_MONTH_LESSON_CHOICES[index][0]
    except (ValueError, IndexError):
        pass
    return "Неизвестный урок"


def get_cancel_keyboard():
    """Клавиатура с кнопкой отмены"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel")]
        ]
    )


def get_homeworks_keyboard():
    """Клавиатура для раздела домашних заданий"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="➕ Новое задание", callback_data="month:2")],
            [types.InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu")]
        ]
    )


def get_pending_tasks_keyboard():
    """Клавиатура для непроверенных заданий"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="✅ Проверенные", callback_data="month:2:checked_tasks")],
            [types.InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu")]
        ]
    )


def get_checked_tasks_keyboard():
    """Клавиатура для проверенных заданий"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="⏳ Непроверенные", callback_data="month:2:pending_tasks")],
            [types.InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu")]
        ]
    )


@month2_router.callback_query(F.data == "month:2:pending_tasks")
async def show_pending_tasks(callback: types.CallbackQuery):
    """Показать непроверенные задания с группировкой по урокам"""
    user_id = callback.from_user.id
    await callback.answer()

    try:
        await callback.message.edit_caption(
            caption="⏳ *Загружаем непроверенные задания...*",
            reply_markup=None,
            parse_mode="Markdown"
        )
        current_message_id = callback.message.message_id
    except Exception:
        new_message = await callback.message.answer_photo(
            photo=photo,
            caption="⏳ *Загружаем непроверенные задания...*",
            reply_markup=None,
            parse_mode="Markdown"
        )
        current_message_id = new_message.message_id

    async with StudentAPI() as student_api:
        student = await student_api.get_student_by_telegram_id(str(user_id))

    if not student:
        try:
            await callback.bot.edit_message_caption(
                chat_id=callback.message.chat.id,
                message_id=current_message_id,
                caption="❌ *Студент не найден*\n\nОбратитесь к администратору",
                reply_markup=get_main_menu(),
                parse_mode="Markdown"
            )
        except Exception:
            await callback.message.answer(
                "❌ Студент не найден",
                reply_markup=get_main_menu()
            )
        return

    async with HWMonth3() as hw_api:
        homeworks = await hw_api.get_homeworks(student_id=student['id'], is_checked=False)

    if not homeworks:
        try:
            await callback.bot.edit_message_caption(
                chat_id=callback.message.chat.id,
                message_id=current_message_id,
                caption="🎉 *Все задания проверены!*\n\nУ вас нет непроверенных домашних заданий ✅",
                reply_markup=get_pending_tasks_keyboard(),
                parse_mode="Markdown"
            )
        except Exception:
            await callback.message.answer(
                "🎉 Все задания проверены!",
                reply_markup=get_pending_tasks_keyboard()
            )
        return

    lessons_dict = {}
    for hw in homeworks:
        lesson_name = hw.get('lesson')
        lesson_display = hw.get('lesson_display', get_lesson_display_name(lesson_name))

        if lesson_name not in lessons_dict:
            lessons_dict[lesson_name] = {
                'display_name': lesson_display,
                'homeworks': []
            }
        lessons_dict[lesson_name]['homeworks'].append(hw)

    text = "⏳ *Непроверенные задания:*\n\n"
    keyboard_buttons = []

    sorted_lessons = sorted(
        lessons_dict.items(),
        key=lambda x: list(dict(TASK_2_MONTH_LESSON_CHOICES).keys()).index(x[0])
        if x[0] in dict(TASK_2_MONTH_LESSON_CHOICES) else 999
    )

    for lesson_name, lesson_data in sorted_lessons:
        lesson_display = lesson_data['display_name']

        for hw in lesson_data['homeworks']:
            hw_id = hw.get('id')
            hw_title = hw.get('title')

            keyboard_buttons.append([
                types.InlineKeyboardButton(
                    text=f"📝 {lesson_display}",
                    callback_data=f"hw2_detail:{hw_id}"
                )
            ])

    text += f"📊 Всего непроверенных: {len(homeworks)} заданий"

    # Добавляем навигационные кнопки
    keyboard_buttons.extend([
        [types.InlineKeyboardButton(text="✅ Проверенные задания", callback_data="month:2:checked_tasks")],
        [types.InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu")]
    ])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    try:
        await callback.bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=current_message_id,
            caption=text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    except Exception:
        await callback.message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )


@month2_router.callback_query(F.data == "month:2:checked_tasks")
async def show_checked_tasks(callback: types.CallbackQuery):
    """Показать проверенные задания с группировкой по урокам"""
    user_id = callback.from_user.id
    await callback.answer()

    try:
        await callback.message.edit_caption(
            caption="⏳ *Загружаем проверенные задания...*",
            reply_markup=None,
            parse_mode="Markdown"
        )
        current_message_id = callback.message.message_id
    except Exception:
        new_message = await callback.message.answer_photo(
            photo=photo,
            caption="⏳ *Загружаем проверенные задания...*",
            reply_markup=None,
            parse_mode="Markdown"
        )
        current_message_id = new_message.message_id

    async with StudentAPI() as student_api:
        student = await student_api.get_student_by_telegram_id(str(user_id))

    if not student:
        try:
            await callback.bot.edit_message_caption(
                chat_id=callback.message.chat.id,
                message_id=current_message_id,
                caption="❌ *Студент не найден*\n\nОбратитесь к администратору",
                reply_markup=get_main_menu(),
                parse_mode="Markdown"
            )
        except Exception:
            await callback.message.answer(
                "❌ Студент не найден",
                reply_markup=get_main_menu()
            )
        return

    async with HWMonth3() as hw_api:
        homeworks = await hw_api.get_homeworks(student_id=student['id'], is_checked=True)

    if not homeworks:
        try:
            await callback.bot.edit_message_caption(
                chat_id=callback.message.chat.id,
                message_id=current_message_id,
                caption="📭 *Проверенных заданий пока нет*\n\nПосле проверки ваши задания появятся здесь 👇",
                reply_markup=get_checked_tasks_keyboard(),
                parse_mode="Markdown"
            )
        except Exception:
            await callback.message.answer(
                "📭 Проверенных заданий пока нет",
                reply_markup=get_checked_tasks_keyboard()
            )
        return

    lessons_dict = {}
    for hw in homeworks:
        lesson_name = hw.get('lesson')
        lesson_display = hw.get('lesson_display', get_lesson_display_name(lesson_name))

        if lesson_name not in lessons_dict:
            lessons_dict[lesson_name] = {
                'display_name': lesson_display,
                'homeworks': []
            }
        lessons_dict[lesson_name]['homeworks'].append(hw)

    # Формируем текст и клавиатуру
    text = "✅ *Проверенные задания:*\n\n"
    keyboard_buttons = []

    # Сортируем уроки по порядку
    sorted_lessons = sorted(
        lessons_dict.items(),
        key=lambda x: list(dict(TASK_2_MONTH_LESSON_CHOICES).keys()).index(x[0])
        if x[0] in dict(TASK_2_MONTH_LESSON_CHOICES) else 999
    )

    for lesson_name, lesson_data in sorted_lessons:
        lesson_display = lesson_data['display_name']
        for hw in lesson_data['homeworks']:
            hw_id = hw.get('id')
            hw_title = hw.get('title')
            grade = hw.get('grade')
            display_title = hw_title[:30] + "..." if len(hw_title) > 30 else hw_title

            if grade:
                if grade >= 9:
                    grade_emoji = "🎯"
                elif grade >= 7:
                    grade_emoji = "👍"
                elif grade >= 5:
                    grade_emoji = "📊"
                else:
                    grade_emoji = "📝"
                button_text = f"{grade_emoji} {lesson_display} ({grade}/10)"
            else:
                button_text = f"📝 {display_title}"

            keyboard_buttons.append([
                types.InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"hw2_detail:{hw_id}"
                )
            ])

        text += "\n"

    total_grades = [hw.get('grade') for hw in homeworks if hw.get('grade')]
    if total_grades:
        overall_avg = sum(total_grades) / len(total_grades)

    keyboard_buttons.extend([
        [types.InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu")]
    ])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    try:
        await callback.bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=current_message_id,
            caption=text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    except Exception:
        await callback.message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )


@month2_router.callback_query(F.data.startswith("hw2_detail:"))
async def show_homework_detail(callback: types.CallbackQuery):
    """Показать детальную информацию о домашнем задании"""
    homework_id = callback.data.split(":")[1]
    await callback.answer()

    try:
        await callback.message.edit_caption(
            caption="⏳ Загружаем информацию о задании...",
            reply_markup=None,
            parse_mode=None  # Отключаем Markdown временно
        )
        current_message_id = callback.message.message_id
    except Exception:
        new_message = await callback.message.answer_photo(
            photo=photo,
            caption="⏳ Загружаем информацию о задании...",
            reply_markup=None,
            parse_mode=None  # Отключаем Markdown временно
        )
        current_message_id = new_message.message_id

    # Получаем детальную информацию о задании
    async with HWMonth3() as hw_api:
        homework = await hw_api.get_homework_by_id(int(homework_id))

    if not homework:
        try:
            await callback.bot.edit_message_caption(
                chat_id=callback.message.chat.id,
                message_id=current_message_id,
                caption="❌ Задание не найдено",
                reply_markup=get_back_to_homeworks_keyboard(),
                parse_mode=None  # Отключаем Markdown
            )
        except Exception:
            await callback.message.answer(
                "❌ Задание не найдено",
                reply_markup=get_back_to_homeworks_keyboard()
            )
        return

    # Функция для экранирования текста
    def escape_markdown(text: str) -> str:
        """Экранирует специальные символы Markdown"""
        if not text:
            return ""
        escape_chars = r'_*[]()~`>#+-=|{}.!'
        return ''.join(['\\' + char if char in escape_chars else char for char in str(text)])

    # Экранируем все текстовые поля
    lesson_display = escape_markdown(homework.get('lesson_display', get_lesson_display_name(homework.get('lesson', ''))))
    title = escape_markdown(homework.get('title', ''))
    task_condition = escape_markdown(homework.get('task_condition', ''))
    github_url = homework.get('github_url', '')  # URL не экранируем
    grade = homework.get('grade')
    is_checked = homework.get('is_checked', False)
    created_at = homework.get('created_at', '')
    originality_check = escape_markdown(homework.get('originality_check', ''))

    # Форматируем дату
    if created_at:
        try:
            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            created_at = dt.strftime("%d.%m.%Y в %H:%M")
        except:
            created_at = "неизвестно"
    created_at = escape_markdown(created_at)

    # Формируем текст с правильным Markdown форматированием
    text = "📚 *Детали задания*\n\n"
    text += f"📝 *Название:* {title}\n"
    text += f"🎯 *Урок:* {lesson_display}\n"
    text += f"📅 *Отправлено:* {created_at}\n\n"

    if task_condition:
        # Обрезаем длинное описание
        if len(task_condition) > 200:
            task_condition = task_condition[:200] + "..."
        text += f"📋 *Описание:* {task_condition}\n\n"

    if github_url:
        text += f"🔗 *GitHub:* {github_url}\n\n"

    # Статус проверки
    if is_checked:
        status_emoji = "✅"
        status_text = "Проверено"
        if grade is not None:
            text += f"{status_emoji} *Статус:* {status_text}\n"
            text += f"📊 *Оценка:* {grade}/10\n"

            if originality_check:
                text += f"📝 *Комментарий:* {originality_check}\n"
    else:
        status_emoji = "⏳"
        status_text = "Ожидает проверки"
        text += f"{status_emoji} *Статус:* {status_text}\n"

    # Создаем клавиатуру
    keyboard_buttons = []

    if github_url:
        keyboard_buttons.append([
            types.InlineKeyboardButton(text="🌐 Открыть GitHub", url=github_url)
        ])

    # Кнопки навигации
    if is_checked:
        keyboard_buttons.append([
            types.InlineKeyboardButton(text="⬅️ К проверенным", callback_data="month:2:checked_tasks")
        ])
    else:
        keyboard_buttons.append([
            types.InlineKeyboardButton(text="⬅️ К непроверенным", callback_data="month:2:pending_tasks")
        ])

    keyboard_buttons.extend([
        [types.InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu")]
    ])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

    try:
        await callback.bot.edit_message_caption(
            chat_id=callback.message.chat.id,
            message_id=current_message_id,
            caption=text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    except Exception as e:
        # Если все еще есть ошибка с Markdown, отправляем без форматирования
        logging.error(f"Markdown error, sending without formatting: {e}")
        try:
            # Создаем текст без Markdown
            text_plain = "📚 Детали задания\n\n"
            text_plain += f"📝 Название: {title}\n"
            text_plain += f"🎯 Урок: {lesson_display}\n"
            text_plain += f"📅 Отправлено: {created_at}\n\n"

            if task_condition:
                text_plain += f"📋 Описание: {task_condition}\n\n"

            if github_url:
                text_plain += f"🔗 GitHub: {github_url}\n\n"

            if is_checked:
                status_emoji = "✅"
                status_text = "Проверено"
                if grade is not None:
                    text_plain += f"{status_emoji} Статус: {status_text}\n"
                    text_plain += f"📊 Оценка: {grade}/10\n"

                    if originality_check:
                        text_plain += f"📝 Комментарий: {originality_check}\n"
            else:
                status_emoji = "⏳"
                status_text = "Ожидает проверки"
                text_plain += f"{status_emoji} Статус: {status_text}\n"

            await callback.bot.edit_message_caption(
                chat_id=callback.message.chat.id,
                message_id=current_message_id,
                caption=text_plain,
                reply_markup=keyboard,
                parse_mode=None  # Отключаем Markdown полностью
            )
        except Exception as final_error:
            logging.error(f"Final error sending message: {final_error}")
            await callback.message.answer_photo(
                photo=photo,
                caption=text_plain,
                reply_markup=keyboard,
                parse_mode=None
            )


def get_back_to_homeworks_keyboard():
    """Клавиатура для возврата к списку заданий"""
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="⏳ Непроверенные", callback_data="month:2:pending_tasks"),
            ],
            [types.InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu")]
        ]
    )