from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram import types
from aiogram_dialog import DialogManager
from api.tasks import create_task
from .states import AddTaskSG


from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format

add_task_dialog = Dialog(
    Window(
        Const("Введите название задачи:"),
        Button(Const("Отмена"), id="cancel"),
        state=AddTaskSG.waiting_for_title
    ),
    Window(
        Const("Введите описание задачи:"),
        Button(Const("Отмена"), id="cancel"),
        state=AddTaskSG.waiting_for_description
    ),
    Window(
        Const("Введите срок выполнения:"),
        Button(Const("Отмена"), id="cancel"),
        state=AddTaskSG.waiting_for_due_date
    ),
    Window(
        Const("Введите категории через запятую:"),
        Button(Const("Отмена"), id="cancel"),
        state=AddTaskSG.waiting_for_categories
    ),
)
