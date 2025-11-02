TASK_1_MONTH_LESSON_CHOICES = [
    ("Введение в Python", "Введение в Python. Переменные, типы данных"),
    ("Условные конструкции", "Условные конструкции (if, else, elif)"),
    ("Циклы", "Циклы for, while"),
    ("Списки", "Списки, срезы, кортежи"),
    ("Словари и множества", "Словари, множества"),
    ("Функции", "Функции, *args, **kwargs"),
    ("Lambda и исключения", "Lambda, исключения"),
    ("Файлы", "Работа с файлами (txt, JSON, CSV)"),
    ("Алгоритмы", "Основы алгоритмов (поиск, сортировка)"),
    ("Мини проект", "Практика: консольное приложение"),
    ("ООП", "Введение в ООП. Классы и объекты"),
    ("Атрибуты и методы", "Атрибуты и методы"),
    ("Наследование", "Наследование, полиморфизм, инкапсуляция"),
    ("Магические методы", "Магические методы"),
    ("RPG проект", "Практика: RPG Game"),
    ("Модули", "Встроенные и собственные модули"),
    ("Окружения", "Виртуальные окружения"),
    ("Регулярки", "Регулярные выражения"),
    ("Финальный проект", "Итоговый проект месяца"),
]

from aiogram import Router, types, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from external_services.api_client_user import StudentAPI, GroupsAPI, HWMonth1
from keyboards.inline_keyboards import get_main_menu, get_teacher_account, return_menu
import logging

month1_router = Router()
photo = types.FSInputFile("img.png")


class Month1HomeworkForm(StatesGroup):
    waiting_for_lesson = State()
    waiting_for_task_condition = State()
    waiting_for_student_answer = State()
    waiting_for_additional_task = State()


def get_lessons_keyboard():
    """Клавиатура для выбора урока"""
    keyboard = []
    for lesson_value, lesson_label in TASK_1_MONTH_LESSON_CHOICES:
        keyboard.append([types.InlineKeyboardButton(
            text=lesson_label,
            callback_data=f"month1_lesson:{lesson_value}"
        )])
    keyboard.append([types.InlineKeyboardButton(
        text="🔙 Назад",
        callback_data="main_menu"
    )])
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_additional_task_keyboard():
    """Клавиатура для добавления дополнительного задания"""
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="✅ Добавить еще задание", callback_data="add_another_task"),
            types.InlineKeyboardButton(text="📤 Отправить на проверку", callback_data="submit_homework")
        ],
        [types.InlineKeyboardButton(text="🔙 Отменить", callback_data="cancel_homework")]
    ])


def get_month1_main_keyboard():
    """Основная клавиатура для 1-го месяца"""
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="📊 Статистика", callback_data="month1:stats"),
            types.InlineKeyboardButton(text="✅ Проверенные", callback_data="month1:checked")
        ],
        [
            types.InlineKeyboardButton(text="⏳ На проверке", callback_data="month1:pending"),
            types.InlineKeyboardButton(text="📝 Сдать ДЗ", callback_data="month1:submit")
        ],
        [
            types.InlineKeyboardButton(text="🔙 Главное меню", callback_data="main_menu")
        ]
    ])


@month1_router.callback_query(F.data == "month:1")
async def handle_month1_main(callback: types.CallbackQuery, bot: Bot):
    """Главное меню 1-го месяца"""
    await callback.message.delete()
    photo = types.FSInputFile("img.png")
    await callback.message.answer_photo(
        photo=photo,
        caption="📘 1-й месяц: Программирование на Python\n\nВыберите действие:",
        reply_markup=get_month1_main_keyboard()
    )
    await callback.answer()


@month1_router.callback_query(F.data == "month1:submit")
async def start_month1_homework(callback: types.CallbackQuery, state: FSMContext):
    """Начало процесса отправки домашнего задания"""
    await callback.message.edit_caption(
        caption="📝 Отправка домашнего задания \n\nВыберите урок, по которому хотите сдать задание:",
        reply_markup=get_lessons_keyboard()
    )
    await state.set_state(Month1HomeworkForm.waiting_for_lesson)
    await callback.answer()


@month1_router.callback_query(F.data.startswith("month1_lesson:"), Month1HomeworkForm.waiting_for_lesson)
async def process_lesson_selection(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора урока"""
    lesson = callback.data.split(":")[1]

    # Находим полное название урока
    lesson_label = next((label for value, label in TASK_1_MONTH_LESSON_CHOICES if value == lesson), lesson)

    await state.update_data(
        lesson=lesson,
        lesson_label=lesson_label,
        main_message_id=callback.message.message_id  # Сохраняем ID основного сообщения
    )

    await callback.message.edit_caption(
        caption=f"📖 **Урок:** {lesson_label}\n\nТеперь введите условие задания, которое вам дали:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🔙 Отменить", callback_data="cancel_homework")]
        ])
    )
    await state.set_state(Month1HomeworkForm.waiting_for_task_condition)
    await callback.answer()


@month1_router.message(Month1HomeworkForm.waiting_for_task_condition)
async def process_task_condition(message: types.Message, state: FSMContext):
    """Обработка условия задания"""
    task_condition = message.text.strip()

    await state.update_data(task_condition=task_condition)

    # Удаляем сообщение пользователя
    await message.delete()

    data = await state.get_data()
    lesson_label = data.get('lesson_label', '')
    main_message_id = data.get('main_message_id')

    # Редактируем существующее сообщение
    await message.bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=main_message_id,
        caption=f"📖 Урок: {lesson_label}\n\n"
                "✅ Условие задания получено!\n\n"
                "📝 Теперь введите ваш ответ/решение задания:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🔙 Отменить", callback_data="cancel_homework")]
        ])
    )

    await state.set_state(Month1HomeworkForm.waiting_for_student_answer)


@month1_router.message(Month1HomeworkForm.waiting_for_student_answer)
async def process_student_answer(message: types.Message, state: FSMContext):
    """Обработка ответа студента"""
    student_answer = message.text or message.caption or ""
    data = await state.get_data()

    if not student_answer.strip():
        await message.answer("❌ Ответ не может быть пустым. Введите ваш ответ:")
        return

    # Удаляем сообщение пользователя
    await message.delete()

    # Сохраняем текущее задание
    current_tasks = data.get('tasks', [])
    current_tasks.append({
        "task_condition": data['task_condition'],
        "student_answer": student_answer.strip()
    })

    await state.update_data(tasks=current_tasks)

    tasks_count = len(current_tasks)
    main_message_id = data.get('main_message_id')

    # Редактируем существующее сообщение
    await message.bot.edit_message_caption(
        chat_id=message.chat.id,
        message_id=main_message_id,
        caption=f"✅ Задание #{tasks_count} добавлено!\n\n"
                "Хотите добавить еще одно задание к этой домашней работе?",
        reply_markup=get_additional_task_keyboard()
    )

    await state.set_state(Month1HomeworkForm.waiting_for_additional_task)


@month1_router.callback_query(F.data == "add_another_task", Month1HomeworkForm.waiting_for_additional_task)
async def add_another_task(callback: types.CallbackQuery, state: FSMContext):
    """Добавление еще одного задания"""
    data = await state.get_data()
    lesson_label = data.get('lesson_label', '')
    main_message_id = data.get('main_message_id')

    # Редактируем существующее сообщение
    await callback.message.edit_caption(
        caption=f"📖 **Урок:** {lesson_label}\n\nВведите условие следующего задания:",
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="🔙 Отменить", callback_data="cancel_homework")]
        ])
    )

    await state.set_state(Month1HomeworkForm.waiting_for_task_condition)
    await callback.answer()


@month1_router.callback_query(F.data == "submit_homework", Month1HomeworkForm.waiting_for_additional_task)
async def submit_homework_final(callback: types.CallbackQuery, state: FSMContext):
    """Финальная отправка домашнего задания"""
    try:
        data = await state.get_data()
        tasks = data.get('tasks', [])
        lesson = data.get('lesson')
        lesson_label = data.get('lesson_label', '')
        main_message_id = data.get('main_message_id')

        if not tasks:
            await callback.message.edit_caption(
                caption="❌ Нет заданий для отправки",
                reply_markup=get_month1_main_keyboard()
            )
            await state.clear()
            return

        # Получаем данные студента
        async with StudentAPI() as student_api:
            student = await student_api.get_student_by_telegram_id(str(callback.from_user.id))

            if not student:
                await callback.message.edit_caption(
                    caption="❌ Студент не найден",
                    reply_markup=get_month1_main_keyboard()
                )
                await state.clear()
                return

            # Отправляем домашку через API
            async with HWMonth1() as hw_api:
                result = await hw_api.create_homework(
                    student_id=student['id'],
                    lesson=lesson,
                    tasks=tasks
                )

                if result:
                    await callback.message.edit_caption(
                        caption=f"✅ Домашнее задание отправлено!\n\n"
                                f"📖 Урок: {lesson_label}\n"
                                f"📝 Заданий: {len(tasks)}\n\n"
                                f"📊 Статус: отправлено на проверку AI\n"
                                f"⏳ Ожидайте результатов проверки!",
                        reply_markup=get_month1_main_keyboard()
                    )
                else:
                    await callback.message.edit_caption(
                        caption=f"❌ Вы уже отправили домашку по уроку {lesson_label}",
                        reply_markup=get_month1_main_keyboard()
                    )

        await state.clear()

    except Exception as e:
        logging.error(f"Error submitting homework: {e}")
        await callback.message.edit_caption(
            caption="❌ Ошибка при отправке домашнего задания",
            reply_markup=get_month1_main_keyboard()
        )
        await state.clear()

    await callback.answer()


@month1_router.callback_query(F.data == "cancel_homework")
async def cancel_homework(callback: types.CallbackQuery, state: FSMContext):
    """Отмена отправки домашнего задания"""
    await state.clear()
    await callback.message.edit_caption(
        caption="❌ Отправка домашнего задания отменена",
        reply_markup=get_month1_main_keyboard()
    )
    await callback.answer()


@month1_router.message(Command("cancel"))
async def cancel_handler(message: types.Message, state: FSMContext):
    """Отмена любого состояния"""
    current_state = await state.get_state()
    if current_state is None:
        return

    # Удаляем сообщение пользователя
    await message.delete()

    data = await state.get_data()
    main_message_id = data.get('main_message_id')

    if main_message_id:
        await message.bot.edit_message_caption(
            chat_id=message.chat.id,
            message_id=main_message_id,
            caption="❌ Действие отменено",
            reply_markup=get_main_menu()
        )

    await state.clear()



@month1_router.callback_query(F.data == "month1:stats")
async def handle_month1_stats(callback: types.CallbackQuery):
    """Статистика по 1-му месяцу"""
    try:
        async with HWMonth1() as hw_api:
            student_api = StudentAPI()
            async with student_api:
                student = await student_api.get_student_by_telegram_id(str(callback.from_user.id))

                if not student:
                    await callback.message.edit_caption(
                        caption="❌ Студент не найден",
                        reply_markup=get_month1_main_keyboard()
                    )
                    return

                stats = await hw_api.get_student_stats(student['id'])

                message_text = f"""
📊 Статистика 1-го месяца

📚 Всего домашних работ: {stats['total_homeworks']}
📝 Всего заданий: {stats['total_tasks']}
✅ Проверено: {stats['checked_tasks']}
⏳ Ожидают проверки: {stats['pending_tasks']}
⭐ Средняя оценка: {stats['average_grade']:.1f}/10

✅ Завершено уроков: {len(stats['completed_lessons'])}
🔄 В процессе: {len(stats['pending_lessons'])}
                """

                await callback.message.edit_caption(
                    caption=message_text,
                    reply_markup=get_month1_main_keyboard()
                )

    except Exception as e:
        logging.error(f"Error getting month1 stats: {e}")
        await callback.message.edit_caption(
            caption="❌ Ошибка при получении статистики",
            reply_markup=get_month1_main_keyboard()
        )
    await callback.answer()


@month1_router.callback_query(F.data == "month1:checked")
async def handle_month1_checked(callback: types.CallbackQuery):
    """Проверенные задания"""
    try:
        async with HWMonth1() as hw_api:
            student_api = StudentAPI()
            async with student_api:
                student = await student_api.get_student_by_telegram_id(str(callback.from_user.id))

                if not student:
                    await callback.message.edit_caption(
                        caption="❌ Студент не найден",
                        reply_markup=get_month1_main_keyboard()
                    )
                    return

                checked_tasks = await hw_api.get_checked_tasks(student['id'])

                if not checked_tasks:
                    await callback.message.edit_caption(
                        caption="✅ Проверенные задания\n\nНет проверенных заданий",
                        reply_markup=get_month1_main_keyboard()
                    )
                    return

                message_text = "✅ Проверенные задания:\n\n"
                keyboard = []

                for i, homework in enumerate(checked_tasks[:10]):  # Ограничиваем 10 работами
                    lesson = homework.get('lesson', 'Неизвестный урок')
                    homework_id = homework.get('id')
                    items = homework.get('items', [])
                    checked_items = [item for item in items if item.get('is_checked')]

                    if checked_items:
                        avg_grade = sum(item.get('grade', 0) for item in checked_items) / len(checked_items)

                        # Создаем кнопку для каждой домашней работы
                        keyboard.append([
                            types.InlineKeyboardButton(
                                text=f"📖 {lesson} | ⭐ {avg_grade:.1f}/10 | 📝 {len(checked_items)}",
                                callback_data=f"month1_hw_detail:{homework_id}"
                            )
                        ])

                # Добавляем кнопку "Назад"
                keyboard.append([
                    types.InlineKeyboardButton(
                        text="🔙 Назад",
                        callback_data="month:1"
                    )
                ])

                if len(checked_tasks) > 10:
                    message_text += f"📋 Показано 10 из {len(checked_tasks)} работ\n"

                await callback.message.edit_caption(
                    caption=message_text,
                    reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
                )

    except Exception as e:
        logging.error(f"Error getting checked tasks: {e}")
        await callback.message.edit_caption(
            caption="❌ Ошибка при получении проверенных заданий",
            reply_markup=get_month1_main_keyboard()
        )
    await callback.answer()


import re

def extract_analysis_text(ai_feedback: str) -> str:
    match = re.search(r"-\*\*Комментарий:\*\*", ai_feedback)
    return match.group(0).strip() if match else ""


@month1_router.callback_query(F.data.startswith("month1_hw_detail:"))
async def handle_homework_detail(callback: types.CallbackQuery):
    """Детальная информация о домашней работе"""
    try:
        homework_id = callback.data.split(":")[1]

        async with HWMonth1() as hw_api:
            homework = await hw_api.get_homework_by_id(homework_id)

            if not homework:
                await callback.answer("❌ Домашняя работа не найдена", show_alert=True)
                return

            lesson = homework.get('lesson', 'Неизвестный урок')
            items = homework.get('items', [])
            checked_items = [item for item in items if item.get('is_checked')]

            if not checked_items:
                await callback.answer("❌ Нет проверенных заданий", show_alert=True)
                return

            # Находим полное название урока
            lesson_label = next((label for value, label in TASK_1_MONTH_LESSON_CHOICES if value == lesson), lesson)

            message_text = f"📖 {lesson_label}\n\n"
            message_text += f"📊 Статус: ✅ Проверено\n"
            message_text += f"📝 Всего заданий: {len(items)}\n"
            message_text += f"✅ Проверено: {len(checked_items)}\n\n"

            # Добавляем информацию по каждому заданию
            for i, item in enumerate(checked_items, 1):
                grade = item.get('grade', 0)
                teacher_comment = item.get('ai_feedback', 'Без комментария')
                message_text += f"Задание {i}:\n"
                message_text += f"⭐ Оценка: {grade}/10\n"
                message_text += f"{teacher_comment.strip().splitlines()[-1]}\n"

                if i < len(checked_items):  # Добавляем разделитель между заданиями
                    message_text += "─" * 30 + "\n\n"

            # Создаем клавиатуру
            keyboard = [
                [types.InlineKeyboardButton(text="🔙 К списку работ", callback_data="month:1")],
                [types.InlineKeyboardButton(text="📊 Главное меню", callback_data="month:1")]
            ]
            try :
                await callback.message.edit_caption(
                    caption=message_text,
                    reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
                )
            except:
                await callback.message.delete()
                await callback.message.answer(
                    text=message_text,
                    reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
                )

    except Exception as e:
        logging.error(f"Error getting homework detail: {e}")
        await callback.answer("❌ Ошибка при загрузке деталей", show_alert=True)


@month1_router.callback_query(F.data == "month1:pending")
async def handle_month1_pending(callback: types.CallbackQuery):
    """Задания на проверке"""
    try:
        async with HWMonth1() as hw_api:
            student_api = StudentAPI()
            async with student_api:
                student = await student_api.get_student_by_telegram_id(str(callback.from_user.id))

                if not student:
                    await callback.message.edit_caption(
                        caption="❌ Студент не найден",
                        reply_markup=get_month1_main_keyboard()
                    )
                    return

                pending_tasks = await hw_api.get_pending_tasks(student['id'])

                if not pending_tasks:
                    await callback.message.edit_caption(
                        caption="⏳ Задания на проверке\n\nВсе задания проверены! 🎉",
                        reply_markup=get_month1_main_keyboard()
                    )
                    return

                message_text = "⏳ **Задания на проверке:**\n\n"
                keyboard = []

                for i, homework in enumerate(pending_tasks[:10]):
                    lesson = homework.get('lesson', 'Неизвестный урок')
                    homework_id = homework.get('id')
                    items = homework.get('items', [])
                    pending_count = sum(1 for item in items if not item.get('is_checked'))

                    keyboard.append([
                        types.InlineKeyboardButton(
                            text=f"📖 {lesson} | ⏳ {pending_count} заданий",
                            callback_data=f"month1_hw_pending_detail:{homework_id}"
                        )
                    ])

                keyboard.append([
                    types.InlineKeyboardButton(
                        text="🔙 Назад",
                        callback_data="month:1"
                    )
                ])

                if len(pending_tasks) > 10:
                    message_text += f"📋 Показано 10 из {len(pending_tasks)} работ\n"

                await callback.message.edit_caption(
                    caption=message_text,
                    reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
                )

    except Exception as e:
        logging.error(f"Error getting pending tasks: {e}")
        await callback.message.edit_caption(
            caption="❌ Ошибка при получении заданий на проверке",
            reply_markup=get_month1_main_keyboard()
        )
    await callback.answer()


@month1_router.callback_query(F.data.startswith("month1_hw_pending_detail:"))
async def handle_pending_homework_detail(callback: types.CallbackQuery):
    """Детальная информация о домашней работе на проверке"""
    try:
        homework_id = callback.data.split(":")[1]

        async with HWMonth1() as hw_api:
            homework = await hw_api.get_homework_by_id(homework_id)

            if not homework:
                await callback.answer("❌ Домашняя работа не найдена", show_alert=True)
                return

            lesson = homework.get('lesson', 'Неизвестный урок')
            items = homework.get('items', [])

            # Находим полное название урока
            lesson_label = next((label for value, label in TASK_1_MONTH_LESSON_CHOICES if value == lesson), lesson)

            message_text = f"📖 {lesson_label}\n\n"
            message_text += f"📊 Статус: ⏳ На проверке\n"
            message_text += f"📝 Всего заданий: {len(items)}\n"
            message_text += f"⏳ Ожидают проверки: {sum(1 for item in items if not item.get('is_checked'))}\n\n"

            # Добавляем информацию по каждому заданию
            for i, item in enumerate(items, 1):
                status = "✅ Проверено" if item.get('is_checked') else "⏳ Ожидает"
                grade = item.get('grade', '—')

                message_text += f"**Задание {i}:** {status}\n"
                if item.get('is_checked'):
                    message_text += f"⭐ Оценка: {grade}/10\n"
                message_text += "\n"

            # Создаем клавиатуру
            keyboard = [
                [types.InlineKeyboardButton(text="🔙 К списку работ", callback_data="month1:pending")],
                [types.InlineKeyboardButton(text="📊 Главное меню", callback_data="month:1")]
            ]

            await callback.message.edit_caption(
                caption=message_text,
                reply_markup=types.InlineKeyboardMarkup(inline_keyboard=keyboard)
            )

    except Exception as e:
        logging.error(f"Error getting pending homework detail: {e}")
        await callback.answer("❌ Ошибка при загрузке деталей", show_alert=True)
