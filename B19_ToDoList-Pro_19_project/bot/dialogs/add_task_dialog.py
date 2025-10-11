from datetime import datetime
from aiogram import types
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Button
from aiogram_dialog.widgets.text import Const
from api.tasks import create_task, get_categories
from api.telegramusers import get_telegram_user


class AddTaskSG(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_due_date = State()
    waiting_for_categories = State()


def validate_text(text: str, max_len=200):
    if not text.strip():
        return False, "Текст не может быть пустым!"
    if len(text) > max_len:
        return False, f"Слишком длинный текст! Максимум {max_len} символов."
    return True, ""


def validate_task_data(data: dict):
    errors = []

    title = data.get("title", "").strip()
    if not title:
        errors.append("Название задачи не может быть пустым")
    elif len(title) > 50:
        errors.append("Название задачи слишком длинное (макс. 50 символов)")

    description = data.get("description", "").strip()
    if len(description) > 200:
        errors.append("Описание задачи слишком длинное (макс. 200 символов)")

    category_ids = data.get("category_ids", [])
    if not isinstance(category_ids, list) or len(category_ids) == 0:
        errors.append("Выберите хотя бы одну категорию")

    due_date = data.get("due_date", "").strip()
    try:
        datetime.fromisoformat(due_date.replace("Z", "+00:00"))
    except Exception:
        errors.append("Неверный формат даты. Используйте YYYY-MM-DD или YYYY-MM-DDTHH:MM:SSZ")

    return errors


async def on_title(message: types.Message, widget, dialog_manager: DialogManager):
    valid, error = validate_text(message.text, max_len=50)
    if not valid:
        await message.answer(f"❌ {error}\nВведите название задачи снова:")
        return
    dialog_manager.dialog_data["title"] = message.text
    await dialog_manager.next()


async def on_description(message: types.Message, widget, dialog_manager: DialogManager):
    valid, error = validate_text(message.text)
    if not valid:
        await message.answer(f"❌ {error}\nВведите описание задачи снова:")
        return
    dialog_manager.dialog_data["description"] = message.text
    await dialog_manager.next()


async def on_due_date(message: types.Message, widget, dialog_manager: DialogManager):
    if not message.text.strip():
        await message.answer("❌ Срок не может быть пустым. Попробуйте снова:")
        return
    dialog_manager.dialog_data["due_date"] = message.text
    await dialog_manager.next()


async def on_category_selected(callback: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    selected = dialog_manager.dialog_data.get("category_ids", [])
    cat_id = int(button.widget_id)

    if cat_id not in selected:
        selected.append(cat_id)
    else:
        selected.remove(cat_id)
    dialog_manager.dialog_data["category_ids"] = selected

    categories = await get_categories()
    names = [cat["name"] for cat in categories if cat["id"] in selected]
    text = "Вы выбрали: " + (", ".join(names) if names else "ничего")
    await callback.answer(text, show_alert=True)


async def on_categories_done(callback: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    data = dialog_manager.dialog_data
    user_data = await get_telegram_user(callback.from_user.id)

    errors = validate_task_data({
        "title": data.get("title"),
        "description": data.get("description", ""),
        "category_ids": data.get("category_ids", []),
        "due_date": data.get("due_date")
    })
    if errors:
        await callback.answer("❌ Ошибки:\n" + "\n".join(errors), show_alert=True)
        return

    await create_task(
        owner=user_data['id'],
        title=data["title"],
        description=data.get("description", ""),
        due_date=data.get("due_date"),
        category_ids=data.get("category_ids", [])
    )

    await callback.message.answer(f"✅ Задача '{data['title']}' успешно добавлена!")
    await dialog_manager.done()


async def on_cancel(callback: types.CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.message.answer("❌ Добавление задачи отменено.")
    await dialog_manager.done()


async def create_add_task_dialog():
    categories_list = await get_categories()
    category_buttons = [ Button(Const(cat["name"]), id=str(cat["id"]), on_click=on_category_selected) for cat in categories_list ]
    cancel_button = Button(Const("🚫 Отмена"), id="cancel", on_click=on_cancel)
    done_button = Button(Const("✅ Готово"), id="done", on_click=on_categories_done)

    return Dialog(
        Window(
            Const("✏️ Введите название задачи:"),
            MessageInput(on_title),
            cancel_button,
            state=AddTaskSG.waiting_for_title,
        ),
        Window(
            Const("📝 Введите описание задачи:"),
            MessageInput(on_description),
            cancel_button,
            state=AddTaskSG.waiting_for_description,
        ),
        Window(
            Const("⏰ Введите срок выполнения (например, '2025-10-12T15:00:00')"),
            MessageInput(on_due_date),
            cancel_button,
            state=AddTaskSG.waiting_for_due_date,
        ),
        Window(
            Const("📂 Выберите категории задачи (нажмите, чтобы выбрать/снять):"),
            Group(*category_buttons),
            done_button,
            cancel_button,
            state=AddTaskSG.waiting_for_categories,
        )
    )
