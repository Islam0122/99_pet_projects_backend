from aiogram import Router, F , Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from database.middlewares import update_user_activity
from keyboards import *
from words import *
from database.models import User
from database.database import async_session
from sqlalchemy import select, func


router = Router()

@router.message(F.text == "/start")
async def start(message: Message):
    await update_user_activity(message.from_user.id, message.from_user.username)
    await message.answer_photo(
        photo=FSInputFile("images/image.png"),
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

MANAGER_GROUP_ID = -4985675904

@router.callback_query(F.data == "manager")
async def enroll_click(callback: CallbackQuery,bot:Bot):
    async with async_session() as session:
        stmt = select(User).where(User.tg_id == callback.from_user.id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            user.clicked_enroll = True
            await session.commit()

    await bot.send_message(
        MANAGER_GROUP_ID,
        f"👤 @{callback.from_user.username} хочет записаться на курс!"
    )
    await callback.answer("✅ Ваша заявка отправлена менеджеру!")


@router.callback_query(F.data == "contacts")
async def show_contact(callback: CallbackQuery):
    await callback.message.edit_caption(
        caption=contacts_text,
        reply_markup=contact_keyboards,
        parse_mode="Markdown"
    )

