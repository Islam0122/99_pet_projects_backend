from aiogram import Router, types, F
from keyboards.inline_keyboards import return_menu_kb, tasks_inline_kb,tasks2_inline_kb
from api.tasks import get_tasks_by_telegram_id, get_task_by_id, delete_task, mark_task_done
from api.telegramusers import get_telegram_user,mark_task_done_and_update_user
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dialogs.add_task_dialog import AddTaskSG

tasks_router = Router()


@tasks_router.callback_query(lambda c: c.data == "my_tasks")
async def show_my_tasks(callback: types.CallbackQuery):
    tg_id = callback.from_user.id
    tasks = await get_tasks_by_telegram_id(tg_id)

    if not tasks or all(t["done"] for t in tasks):
        await callback.message.edit_text(text="📭 У вас пока нет невыполненных задач.",reply_markup=return_menu_kb())
        return

    kb = tasks_inline_kb(tasks)
    await callback.message.edit_text(text="📝 Ваши задачи:", reply_markup=kb)


@tasks_router.callback_query(lambda c: c.data == "old_tasks")
async def show_old_tasks(callback: types.CallbackQuery):
    tg_id = callback.from_user.id
    tasks = await get_tasks_by_telegram_id(tg_id)
    done_tasks = [t for t in tasks if t.get("done")]

    if not done_tasks:
        await callback.message.edit_text(
            text="📭 У вас пока нет выполненных задач.",
            reply_markup=return_menu_kb()
        )
        return

    kb = tasks2_inline_kb(done_tasks)
    await callback.message.edit_text(
        text="📝 Ваши выполненные задачи:",
        reply_markup=kb
    )


@tasks_router.callback_query(lambda c: c.data.startswith("task_"))
async def task_actions(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    task = await get_task_by_id(task_id)

    if not task:
        await callback.message.answer("❌ Задача не найдена.")
        return

    status = "✅ Выполнена" if task["done"] else "❌ Не выполнена"
    due = task.get("due_date_formatted") or "нет"

    categories = ", ".join([c["name"] for c in task.get("categories", [])]) or "Нет категорий"

    text = (
        f"⚡ Задача ID {task_id}\n\n"
        f"📌 Название: {task['title']}\n"
        f"📝 Описание: {task.get('description', 'Нет описания')}\n"
        f"🏷 Категории: {categories}\n"
        f"⏰ Срок: {due}\n"
        f"🕒 Создано: {task.get('created_at', 'Нет данных')}\n"
        f"Статус: {status}"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Выполнено", callback_data=f"done_{task_id}"),
        ],
        [
            InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_{task_id}"),
            InlineKeyboardButton(text="🔙 Назад", callback_data="my_tasks")
        ]
    ])

    await callback.message.edit_text(text=text, reply_markup=kb)


@tasks_router.callback_query(lambda c: c.data.startswith("delete_"))
async def delete_task_callback(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    await delete_task(task_id)
    await callback.message.edit_text(text=f"🗑 Задача ID {task_id} удалена.",reply_markup=return_menu_kb())


@tasks_router.callback_query(lambda c: c.data.startswith("done_"))
async def mark_done_callback(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    await mark_task_done(task_id)
    user_data = await get_telegram_user(callback.from_user.id)
    user_stats = await mark_task_done_and_update_user(user_data['id'])

    await callback.message.edit_text(
        text=(
            f"✅ Задача ID {task_id} выполнена!\n\n"
            f"Всего выполнено: {user_stats['total_task_completes']}\n"
            f"Streak дней: {user_stats['streak_days']}"
        ),
        reply_markup=return_menu_kb()
    )


@tasks_router.callback_query(lambda c: c.data == "add_task")
async def add_tasks(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="✏️ Чтобы добавить задачу, напишите /add или нажмите кнопку ниже:",
        reply_markup=return_menu_kb()
    )
    await callback.answer()

