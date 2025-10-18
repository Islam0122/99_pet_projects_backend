import base64
import json
import os
import uuid
from io import BytesIO

import requests
from aiogram import Bot, types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv, find_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv(find_dotenv())

CLIENT_ID = '71b92890-bf91-4b6b-9645-6561b93e3d7d'
SECRET = '3278c7e4-6c0c-4b7b-a8b7-9baadb679504'

ai_help_private_router = Router()


def get_access_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
    }
    payload = {"scope": "GIGACHAT_API_PERS"}

    try:
        res = requests.post(
            url=url,
            headers=headers,
            auth=HTTPBasicAuth(CLIENT_ID, SECRET),
            data=payload,
            verify=False,
        )
        res.raise_for_status()
        access_token = res.json().get("access_token")
        if not access_token:
            raise ValueError("Токен доступа не был получен.")
        return access_token
    except requests.RequestException as e:
        print("Ошибка при получении access token:", e)
        return None


def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": msg,
            }
        ],
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        print("Ошибка при отправке запроса к GigaChat API:", e)
        return "Ошибка при получении ответа от GigaChat."


def sent_prompt_and_get_response(system_prompt: str, user_question: str):
    """Отправка промпта с системной инструкцией и вопросом пользователя"""
    access_token = get_access_token()

    if access_token:
        # Собираем полный промпт с системной инструкцией
        full_prompt = f"{system_prompt}\n\nВопрос пользователя: {user_question}"
        response = send_prompt(full_prompt, access_token)
        return response
    else:
        return "Не удалось получить access token."


class AiAssistanceState(StatesGroup):
    WaitingForQuestion = State()


def get_cancel_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_ai_help")]
        ]
    )


def get_ai_help_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📚 Совет по книге", callback_data="ai_book_advice")],
            [InlineKeyboardButton(text="💪 Мотивация", callback_data="ai_motivation")],
            [InlineKeyboardButton(text="❓ Викторина", callback_data="ai_quiz")],
            [InlineKeyboardButton(text="🔄 Другой вопрос", callback_data="ai_help")],
            [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
        ]
    )


def get_ai_categories_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📚 Совет по книге", callback_data="ai_book_advice")],
            [InlineKeyboardButton(text="💪 Мотивация", callback_data="ai_motivation")],
            [InlineKeyboardButton(text="❓ Викторина", callback_data="ai_quiz")],
            [InlineKeyboardButton(text="💬 Общий вопрос", callback_data="ai_help")],
            [InlineKeyboardButton(text="⏪ Главное меню", callback_data="main_menu")]
        ]
    )


@ai_help_private_router.callback_query(F.data == "ai_help")
async def send_ai_help_request(query: types.CallbackQuery, state: FSMContext) -> None:
    """Начало диалога с AI помощником"""
    await state.update_data(ai_message_id=query.message.message_id)

    try:
        await query.message.edit_text(
            text=(
                "🤖 <b>Readify AI Помощник</b>\n\n"
                "Я ваш персональный помощник по чтению! 🎯\n\n"
                "Могу помочь с:\n"
                "• 📚 Советами по книгам и чтению\n"
                "• 💪 Мотивацией для регулярного чтения\n"
                "• ❓ Викторинами и вопросами по литературе\n"
                "• 🔍 Ответами на вопросы о книгах\n\n"
                "📝 <i>Задайте ваш вопрос или выберите категорию:</i>"
            ),
            reply_markup=get_ai_categories_kb(),
            parse_mode="HTML"
        )
    except Exception as e:
        await query.message.delete()
        new_msg = await query.message.answer(
            text=(
                "🤖 <b>Readify AI Помощник</b>\n\n"
                "Я ваш персональный помощник по чтению! 🎯\n\n"
                "Могу помочь с:\n"
                "• 📚 Советами по книгам и чтению\n"
                "• 💪 Мотивацией для регулярного чтения\n"
                "• ❓ Викторинами и вопросами по литературе\n"
                "• 🔍 Ответами на вопросами о книгах\n\n"
                "📝 <i>Задайте ваш вопрос или выберите категорию:</i>"
            ),
            reply_mup=get_ai_categories_kb(),
            parse_mode="HTML"
        )
        await state.update_data(ai_message_id=new_msg.message_id)

    await state.set_state(AiAssistanceState.WaitingForQuestion)
    await query.answer()


@ai_help_private_router.callback_query(F.data == "ai_book_advice")
async def ai_book_advice_handler(query: types.CallbackQuery, state: FSMContext):
    """Советы по книгам"""
    await state.update_data(ai_message_id=query.message.message_id)

    try:
        await query.message.edit_text(
            text=(
                "📚 <b>Советы по книгам</b>\n\n"
                "Расскажите о ваших предпочтениях в чтении, и я порекомендую книги или дам советы!\n\n"
                "Примеры:\n"
                "• «Посоветуй книги в жанре фэнтези»\n"
                "• «Какую книгу почитать после Гарри Поттера?»\n"
                "• «Нужна помощь с пониманием классической литературы»\n\n"
                "📝 <i>Опишите ваши предпочтения:</i>"
            ),
            reply_markup=get_cancel_kb(),
            parse_mode="HTML"
        )
    except Exception as e:
        await query.message.delete()
        new_msg = await query.message.answer(
            text=(
                "📚 <b>Советы по книгам</b>\n\n"
                "Расскажите о ваших предпочтениях в чтении, и я порекомендую книги или дам советы!\n\n"
                "📝 <i>Опишите ваши предпочтения:</i>"
            ),
            reply_markup=get_cancel_kb(),
            parse_mode="HTML"
        )
        await state.update_data(ai_message_id=new_msg.message_id)

    await state.set_state(AiAssistanceState.WaitingForQuestion)
    await query.answer()


@ai_help_private_router.callback_query(F.data == "ai_motivation")
async def ai_motivation_handler(query: types.CallbackQuery, state: FSMContext):
    """Мотивация для чтения"""
    await state.update_data(ai_message_id=query.message.message_id)

    try:
        await query.message.edit_text(
            text=(
                "💪 <b>Мотивация для чтения</b>\n\n"
                "Нужна мотивация чтобы начать или продолжить читать? Я помогу! 🚀\n\n"
                "Расскажите о вашей ситуации:\n"
                "• «Трудно найти время для чтения»\n"
                "• «Потерял интерес к книгам»\n"
                "• «Хочу выработать привычку читать регулярно»\n\n"
                "📝 <i>Опишите вашу ситуацию:</i>"
            ),
            reply_markup=get_cancel_kb(),
            parse_mode="HTML"
        )
    except Exception as e:
        await query.message.delete()
        new_msg = await query.message.answer(
            text=(
                "💪 <b>Мотивация для чтения</b>\n\n"
                "Нужна мотивация чтобы начать или продолжить читать? Я помогу! 🚀\n\n"
                "📝 <i>Опишите вашу ситуацию:</i>"
            ),
            reply_markup=get_cancel_kb(),
            parse_mode="HTML"
        )
        await state.update_data(ai_message_id=new_msg.message_id)

    await state.set_state(AiAssistanceState.WaitingForQuestion)
    await query.answer()


@ai_help_private_router.callback_query(F.data == "ai_quiz")
async def ai_quiz_handler(query: types.CallbackQuery, state: FSMContext):
    """Викторины по литературе"""
    await state.update_data(ai_message_id=query.message.message_id)

    try:
        await query.message.edit_text(
            text=(
                "❓ <b>Литературная викторина</b>\n\n"
                "Давайте проверим ваши знания литературы! 📖\n\n"
                "Вы можете:\n"
                "• Попросить викторину по определенному автору или жанру\n"
                "• Пройти тест на знание классики\n"
                "• Получить вопросы по конкретной книге\n\n"
                "📝 <i>О чем хотите викторину?</i>"
            ),
            reply_markup=get_cancel_kb(),
            parse_mode="HTML"
        )
    except Exception as e:
        await query.message.delete()
        new_msg = await query.message.answer(
            text=(
                "❓ <b>Литературная викторина</b>\n\n"
                "Давайте проверим ваши знания литературы! 📖\n\n"
                "📝 <i>О чем хотите викторину?</i>"
            ),
            reply_markup=get_cancel_kb(),
            parse_mode="HTML"
        )
        await state.update_data(ai_message_id=new_msg.message_id)

    await state.set_state(AiAssistanceState.WaitingForQuestion)
    await query.answer()


@ai_help_private_router.message(AiAssistanceState.WaitingForQuestion)
async def process_ai_help_request(message: types.Message, state: FSMContext, bot: Bot):
    """Обработка вопроса пользователя"""
    data = await state.get_data()
    ai_message_id = data.get('ai_message_id')

    # Удаляем сообщение пользователя
    await message.delete()

    try:
        # Обновляем сообщение - показываем обработку
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=ai_message_id,
            text=(
                "🤖 <b>Readify AI Помощник</b>\n\n"
                "⏳ <i>Анализирую ваш запрос...</i>\n\n"
                f"📝 <b>Ваш вопрос:</b> {message.text[:100]}..."
            ),
            reply_markup=None,
            parse_mode="HTML"
        )

        # Системный промпт для специализации на книгах и мотивации
        system_prompt = """Ты - AI помощник в боте Readify, который специализируется на книгах, чтении и мотивации. 

Твоя роль:
1. Давать советы по книгам и рекомендации для чтения
2. Предоставлять мотивацию и советы по развитию привычки чтения
3. Создавать викторины и вопросы по литературе
4. Помогать с выбором книг и решением проблем связанных с чтением

Отвечай дружелюбно, вдохновляюще и полезно. Фокусируйся на теме книг и чтения. 
Если вопрос не связан с книгами, вежливо предложи перейти к литературной теме.

Будь креативным в викторинах и мотивационных советах!"""

        # Генерируем ответ через GigaChat с специализированным промптом
        generated_response = sent_prompt_and_get_response(system_prompt, message.text)

        # Обрезаем ответ если слишком длинный
        if len(generated_response) > 3000:
            generated_response = generated_response[:3000] + "...\n\n⚠️ <i>Ответ сокращен</i>"

        # Обновляем сообщение с ответом
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=ai_message_id,
            text=(
                "🤖 <b>Readify AI Помощник</b>\n\n"
                f"📝 <b>Ваш вопрос:</b> {message.text}\n\n"
                f"💡 <b>Ответ:</b>\n{generated_response}"
            ),
            reply_markup=get_ai_help_kb(),
            parse_mode="HTML"
        )

    except Exception as e:
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=ai_message_id,
                text=(
                    "🤖 <b>Readify AI Помощник</b>\n\n"
                    "❌ <b>Произошла ошибка</b>\n\n"
                    "Не удалось получить ответ. Попробуйте позже."
                ),
                reply_markup=get_ai_help_kb(),
                parse_mode="HTML"
            )
        except Exception:
            pass
        print(f"Ошибка при обработке AI запроса: {e}")

    await state.clear()


@ai_help_private_router.callback_query(F.data == "cancel_ai_help")
async def cancel_ai_help(query: types.CallbackQuery, state: FSMContext):
    """Отмена AI помощи"""
    await state.clear()

    try:
        await query.message.edit_text(
            text="❌ <b>AI помощь отменена</b>",
            reply_markup=get_ai_categories_kb(),
            parse_mode="HTML"
        )
    except Exception as e:
        await query.message.delete()
        await query.message.answer(
            text="❌ <b>AI помощь отменена</b>",
            reply_markup=get_ai_categories_kb(),
            parse_mode="HTML"
        )

    await query.answer()


# Обработчик команды /ai
@ai_help_private_router.message(F.text == "/ai")
async def ai_command_handler(message: types.Message, state: FSMContext, bot: Bot):
    """Обработчик команды /ai"""
    await message.delete()

    start_msg = await message.answer(
        text=(
            "🤖 <b>Readify AI Помощник</b>\n\n"
            "Я ваш персональный помощник по чтению! 🎯\n\n"
            "Могу помочь с:\n"
            "• 📚 Советами по книгам и чтению\n"
            "• 💪 Мотивацией для регулярного чтения\n"
            "• ❓ Викторинами и вопросами по литературе\n"
            "• 🔍 Ответами на вопросы о книгах\n\n"
            "📝 <i>Задайте ваш вопрос или выберите категорию:</i>"
        ),
        reply_markup=get_ai_categories_kb(),
        parse_mode="HTML"
    )

    await state.update_data(ai_message_id=start_msg.message_id)
    await state.set_state(AiAssistanceState.WaitingForQuestion)