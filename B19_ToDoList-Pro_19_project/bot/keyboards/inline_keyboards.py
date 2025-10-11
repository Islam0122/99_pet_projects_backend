from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧑 Профиль", callback_data="profile")],
            [InlineKeyboardButton(text="📌 Мои текущие задачи", callback_data="my_tasks")],
            [InlineKeyboardButton(text="✅ Выполненные задачи", callback_data="old_tasks")],
            [InlineKeyboardButton(text="➕ Добавить задачу", callback_data="add_task")],
        ]
    )

def return_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu")]
        ]
    )

def tasks_inline_kb(tasks: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for idx, task in enumerate(tasks, start=1):
        if not task["done"]:
            kb.inline_keyboard.append([
                InlineKeyboardButton(
                    text=f"{idx}. {task['title']}",
                    callback_data=f"task_{task['id']}"
                )
            ])
    kb.inline_keyboard.append([
        InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu")
    ])
    return kb

def tasks2_inline_kb(tasks: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for idx, task in enumerate(tasks, start=1):
        if task["done"]:
            kb.inline_keyboard.append([
                InlineKeyboardButton(
                    text=f"{idx}. {task['title']} ✅",
                    callback_data=f"task_{task['id']}"
                )
            ])
    kb.inline_keyboard.append([
        InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="main_menu")
    ])
    return kb
