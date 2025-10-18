# import base64
# import json
# import os
# import uuid
# from io import BytesIO
#
# import requests
# from aiogram import Bot, types
# from dotenv import load_dotenv, find_dotenv
# from requests.auth import HTTPBasicAuth
#
# load_dotenv(find_dotenv())
#
# CLIENT_ID = '71b92890-bf91-4b6b-9645-6561b93e3d7d'
# SECRET = '3278c7e4-6c0c-4b7b-a8b7-9baadb679504'
#
#
# def get_access_token() -> str:
#     url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
#     headers = {
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Accept': 'application/json',
#         'RqUID': str(uuid.uuid4()),  # уникальный идентификатор запроса
#     }
#     payload = {"scope": "GIGACHAT_API_PERS"}
#
#     try:
#         res = requests.post(
#             url=url,
#             headers=headers,
#             auth=HTTPBasicAuth(CLIENT_ID, SECRET),
#             data=payload,
#             verify=False,  # Убедитесь, что использование verify=False безопасно для вашей среды
#         )
#         res.raise_for_status()  # проверка на наличие ошибок
#         access_token = res.json().get("access_token")
#         if not access_token:
#             raise ValueError("Токен доступа не был получен.")
#         return access_token
#     except requests.RequestException as e:
#         print("Ошибка при получении access token:", e)
#         return None
#
#
# def send_prompt(msg: str, access_token: str):
#     url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
#     payload = json.dumps({
#         "model": "GigaChat",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": msg,
#             }
#         ],
#     })
#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json',
#         'Authorization': f'Bearer {access_token}'
#     }
#
#     try:
#         response = requests.post(url, headers=headers, data=payload, verify=False)
#         response.raise_for_status()  # проверка на наличие ошибок
#         return response.json()["choices"][0]["message"]["content"]
#     except requests.RequestException as e:
#         print("Ошибка при отправке запроса к GigaChat API:", e)
#         return "Ошибка при получении ответа от GigaChat."
#
#
#
# def sent_prompt_and_get_response(msg: str):
#     access_token = get_access_token()
#
#     if access_token:
#         response = send_prompt(msg, access_token)
#         decorated_response = f'✨ {response} 🌟️'
#         return decorated_response
#     else:
#         return "Не удалось получить access token."
#
#
#
#
#
# ai_help_private_router = Router()
# ai_help_private_router.message.filter(ChatTypeFilter(['private']))
#
#
# # Переименованный класс состояния
# class AiAssistanceState(StatesGroup):
#     WaitingForReview = State()
#
#
# @ai_help_private_router.callback_query(F.data.startswith("ai_help"))
# async def send_review_request_callback_query(query: types.CallbackQuery, state: FSMContext) -> None:
#     user_id = query.from_user.id
#     language = user_preferences.get(user_id, {}).get('language', 'kgz')
#
#     await query.message.edit_caption(
#         caption=messages[language]['ai_help_message'],
#         reply_markup=get_cancel_keyboard(language)
#     )
#     await state.set_state(AiAssistanceState.WaitingForReview)  # Используем новое имя состояния
#
#
# @ai_help_private_router.callback_query(F.data == "cancel_ai_help")
# async def cancel_feedback(query: types.CallbackQuery, state: FSMContext) -> None:
#     user_id = query.from_user.id
#     language = user_preferences.get(user_id, {}).get('language', 'ru')
#     await state.clear()
#     await query.message.edit_caption(caption=messages[language]['request_canceled'],
#                                      reply_markup=start_functions_keyboard(language))
#
#
# # Переименованная функция
# @ai_help_private_router.message(AiAssistanceState.WaitingForReview)  # Используем новое имя класса состояния
# async def process_help_request(message: types.Message, state: FSMContext, bot: Bot):
#     language = user_preferences.get(message.from_user.id, {}).get('language', 'ru')
#
#     if message.text:
#         generated_help = sent_prompt_and_get_response(message.text)
#         await message.answer(generated_help, reply_markup=ReplyKeyboardRemove())
#         await state.clear()
#         await message.answer(messages[language]['review_sent'], reply_markup=start_functions_keyboard(language))
#     else:
#         keyboard = InlineKeyboardBuilder()
#         keyboard.add(InlineKeyboardButton(text=cancel[language], callback_data="cancel_create_feedback"))
#         await message.answer(messages[language]['review_invalid'], reply_markup=keyboard.as_markup())