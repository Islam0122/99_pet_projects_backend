from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def echo_message(message: Message):
    await message.answer(f"Ты написал: {message.text}")
