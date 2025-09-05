from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="ℹ️ Об академии", callback_data="about_us"),
            InlineKeyboardButton(text="🎓 Курсы", callback_data="courses"),
        ],
        [
            InlineKeyboardButton(text="💡 Почему стоит учиться у нас?", callback_data="advantages"),
        ],
        [
            InlineKeyboardButton(text="📞 Контакты", callback_data="contacts"),
        ],
        [
            InlineKeyboardButton(text="🚀 Записаться на курс", callback_data="manager"),
        ],
    ]
)

return_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📞 Контакты", callback_data="contacts"),
            InlineKeyboardButton(text="🚀 Записаться на курс", callback_data="manager"),
        ],
        [
            InlineKeyboardButton(text="⬅️ В меню", callback_data="main_menu"),
        ],
    ]
)

about_us_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👨‍🏫 Наши преподаватели", callback_data="teachers"),
        ],
        [
            InlineKeyboardButton(text="🎓 Курсы", callback_data="courses"),
        ],
        [
            InlineKeyboardButton(text="📞 Контакты", callback_data="contacts"),
            InlineKeyboardButton(text="🚀 Записаться на курс", callback_data="manager"),
        ],
        [
            InlineKeyboardButton(text="⬅️ В меню", callback_data="main_menu"),
        ],
    ]
)

courses_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🖥 Backend Bootcamp", callback_data="course:backend"),
            InlineKeyboardButton(text="💻 Frontend Bootcamp", callback_data="course:frontend"),
        ],
        [
            InlineKeyboardButton(text="⬅️ В меню", callback_data="main_menu"),
        ],
    ]
)
