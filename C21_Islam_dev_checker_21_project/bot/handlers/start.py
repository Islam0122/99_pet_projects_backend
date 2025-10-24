from aiogram import Router, types, Bot,F
from aiogram.filters import Command
from external_services.api_client_user import StudentAPI, GroupsAPI
from keyboards.inline_keyboards import get_main_menu,get_teacher_account,return_menu
import logging

start_router = Router()
photo = types.FSInputFile("img.png")

WELCOME_TEXT = (
    "👋 Добро пожаловать в *IslamDev Checker* - систему мониторинга учебного прогресса!\n\n"
    "📚 Возможности для тебя:\n"
    "• 👤 Просмотр своего профиля и личной статистики\n"
    "• 📝 Отправка домашних заданий\n"
    "• ✅ Просмотр выполненных и проверенных заданий\n"
    "• 📊 Отслеживание рейтинга в Academy\n\n"
    "👇 Используй кнопки меню ниже для навигации по боту."
)



SYSTEM_UNAVAILABLE_TEXT = """
⚠️ Система временно недоступна

Мы работаем над восстановлением работы.
Попробуйте позже или обратитесь к администратору.
"""


async def get_user_group_info(telegram_id: str, bot: Bot) -> dict:
    """
    Получает информацию о группах пользователя и создает студента если нужно
    """
    try:
        async with GroupsAPI() as groups_api:
            groups = await groups_api.get_all_groups()

            if groups is None:
                logging.error("API is unavailable")
                return {'has_access': False, 'group_found': None, 'student_created': False}

            if not groups:
                logging.warning("No groups found in system")
                return {'has_access': False, 'group_found': None, 'student_created': False}

            # Ищем группу где есть пользователь
            for group in groups:
                group_telegram_id = group.get('telegram_id')
                if not group_telegram_id:
                    continue

                try:
                    chat_member = await bot.get_chat_member(
                        chat_id=group_telegram_id,
                        user_id=int(telegram_id)
                    )

                    if chat_member.status not in ['left', 'kicked', 'restricted']:
                        logging.info(f"User {telegram_id} found in group {group_telegram_id}")

                        # Проверяем, есть ли пользователь уже в базе как студент
                        async with StudentAPI() as student_api:
                            existing_student = await student_api.get_student_by_telegram_id(telegram_id)

                            if not existing_student:
                                # Создаем нового студента
                                student_created = await create_student_in_group(
                                    telegram_id=telegram_id,
                                    group_data=group,
                                    chat_member=chat_member
                                )
                                return {
                                    'has_access': True,
                                    'group_found': group,
                                    'student_created': student_created
                                }
                            else:
                                # Студент уже существует
                                return {
                                    'has_access': True,
                                    'group_found': group,
                                    'student_created': False
                                }

                except Exception as e:
                    logging.warning(f"Error checking user in group {group_telegram_id}: {e}")
                    continue

            logging.info(f"User {telegram_id} not found in any group")
            return {'has_access': False, 'group_found': None, 'student_created': False}

    except Exception as e:
        logging.error(f"Error checking user access: {e}")
        return {'has_access': False, 'group_found': None, 'student_created': False}


async def create_student_in_group(telegram_id: str, group_data: dict, chat_member) -> bool:
    """
    Создает нового студента в группе
    """
    try:
        async with StudentAPI() as student_api:
            # Получаем информацию о пользователе из Telegram
            user = chat_member.user
            full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
            if not full_name:
                full_name = f"User_{telegram_id}"

            username = user.username

            # Подготавливаем данные для создания студента
            student_data = {
                "full_name": full_name,
                "telegram_id": telegram_id,
                "username": username,
                "group": group_data['id'],  # ID группы из базы данных
                "is_active": True,
                "total_homeworks": 0,
                "completed_homeworks": 0,
                "average_score": 0.0,
                "best_score": 0.0,
                "total_points": 0.0,
                "rank": 0,
                "progress_level": "Новичок"
            }

            # Создаем студента
            result = await student_api.create_student(student_data)

            if result:
                logging.info(f"Successfully created student {telegram_id} in group {group_data['title']}")
                return True
            else:
                logging.error(f"Failed to create student {telegram_id}")
                return False

    except Exception as e:
        logging.error(f"Error creating student {telegram_id}: {e}")
        return False


async def update_student_username(telegram_id: str, username: str):
    """
    Обновляет username студента если он изменился
    """
    try:
        async with StudentAPI() as student_api:
            # Используем правильный метод get_student_by_telegram_id
            student = await student_api.get_student_by_telegram_id(telegram_id)
            if student and student.get('username') != username:
                await student_api.update_student(telegram_id, {"username": username})
                logging.info(f"Updated username for student {telegram_id}")
    except Exception as e:
        logging.warning(f"Could not update username for {telegram_id}: {e}")


@start_router.message(Command("start"))
async def cmd_start(message: types.Message, bot: Bot):
    user_telegram_id = str(message.from_user.id)
    username = message.from_user.username

    try:
        # Получаем информацию о доступе и создаем студента если нужно
        access_info = await get_user_group_info(user_telegram_id, bot)

        if access_info['has_access']:
            # Формируем приветственное сообщение
            group_title = access_info['group_found'].get('title', 'неизвестной группе') if access_info[
                'group_found'] else 'группе'

            greeting = f"{WELCOME_TEXT}"

            await message.answer_photo(photo=photo,caption=greeting, reply_markup=get_main_menu(),parse_mode="Markdown")

            if username:
                await update_student_username(user_telegram_id, username)

        else:

            await message.answer_photo(
                photo=photo,
                caption="❌ Доступ запрещен!\n\n"
                f"Ваш Telegram ID: {user_telegram_id}\n"
                f"Username: @{username if username else 'не установлен'}\n\n"
                f"Для получения доступа необходимо:\n"
                f"1. Быть участником учебной Telegram-группы\n"
                f"2. Группа должна быть добавлена в систему\n\n"
                f"📍 Обратитесь к вашему преподавателю.",
                reply_markup=get_teacher_account()
            )

    except Exception as e:
        logging.error(f"Error in /start command: {e}")
        await message.answer(
            SYSTEM_UNAVAILABLE_TEXT + f"\n\nОшибка: {str(e)}",
            reply_markup=types.ReplyKeyboardRemove()
        )


@start_router.callback_query(F.data == "main_menu")
async def main_menu(callback: types.CallbackQuery):
    try:
        await callback.message.edit_caption(caption=WELCOME_TEXT, reply_markup=get_main_menu())
    except:
        await callback.message.delete()
        await callback.message.answer_photo(photo=photo, caption=WELCOME_TEXT, reply_markup=get_main_menu(),parse_mode="Markdown")


ABOUT_TEXT = """
✨ IslamDev Checker — твой помощник для контроля учебного прогресса и домашних заданий

📚 Что можно делать:
• Просматривать свой профиль и личную статистику
• Отправлять домашние задания прямо через Telegram
• Проверять выполненные и проверенные задания
• Отслеживать рейтинг среди студентов
• Получать прогнозы по темам, которые стоит повторить

💡 О проекте:
Разработан для студентов автором Islam Duishobaev (@islam_duishobaev)

🚀 Учись эффективно, следи за прогрессом и достигай своих целей вместе с IslamDev Checker
"""


@start_router.callback_query(F.data == "menu:about")
async def about_bot(callback: types.CallbackQuery):
    try:
        await callback.message.edit_caption(
            caption=ABOUT_TEXT,
            reply_markup=return_menu(),
        )
    except Exception:
        await callback.message.delete()
        await callback.message.answer_photo(
            photo=photo,
            caption=ABOUT_TEXT,
            reply_markup=return_menu(),
        )


TEACHER_TEXT = """
🟩🟩🟩 **Преподаватель: Islam Duishobaev** 🟩🟩🟩

🎯 **Профиль:**
➡ 💻Backend | ⚡Frontend |🤖TelegramBot
➡ 💡Backend -->  Python, Django, DRF, FastAPI  🪄  
➡ 🤖Telegram-bot --> Aiogram
➡ 🖥 Frontend: React, Redux, TypeScript, JS 

📌 **Об авторе:**
🔹 Опытный наставник по Python, Django и разработке Telegram-ботов  
🔹 Создатель системы *IslamDev Checker* для мониторинга прогресса студентов  
🔹 Всегда на связи в Telegram: [@islam_duishobaev](https://t.me/islam_duishobaev)

🚀 **Миссия:**
Помогать студентам эффективно учиться, отслеживать прогресс и достигать учебных целей  

💡 **Совет от преподавателя:**  
Учись регулярно, используй практику и не бойся экспериментировать!
"""


@start_router.callback_query(F.data == "menu:about_teacher")
async def teacher(callback: types.CallbackQuery):
    try:
        await callback.message.edit_caption(
            caption=TEACHER_TEXT,
            reply_markup=return_menu(),
            parse_mode="Markdown"
        )
    except Exception:
        await callback.message.delete()
        await callback.message.answer(
            text=TEACHER_TEXT,
            reply_markup=return_menu(),
            parse_mode="Markdown"
        )


