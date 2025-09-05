from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from keyboards import *
from words import *

router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await message.answer_photo(
        photo=FSInputFile("image.png"),
        caption=welcome_message,
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )


@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=welcome_message,
        reply_markup=main_keyboard,
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "about_us")
async def about_us(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=ABOUT,
        reply_markup=about_us_keyboard,
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "courses")
async def courses(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=courses_text,
        reply_markup=courses_keyboard,
        parse_mode="Markdown",
    )


@router.callback_query(F.data.startswith("course:"))
async def course_info(callback: CallbackQuery):
    course = callback.data.split(":")[1]

    if course == "backend":
        text = backend_text
    elif course == "frontend":
        text = frontend_text
    else:
        text = "Информация недоступна."

    await callback.message.edit_caption(
        caption=text,
        reply_markup=return_keyboard,
        parse_mode="Markdown"
    )



@router.callback_query(F.data == "advantages")
async def show_advantages(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=advantages_text,
        reply_markup=return_keyboard,
        parse_mode="Markdown"
    )
