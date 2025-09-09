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


admin_main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
        ],
    ]
)

admin_back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="admin_menu"),
        ]
    ]
)

contact_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📱 WhatsApp", url="http://wa.me/996501001112"),
            InlineKeyboardButton(text="📷 Instagram", url="https://www.instagram.com/fullcode.kg?igsh=Yno5aXNvam9oMHpi"),
        ],
        [
            InlineKeyboardButton(text="🚀 Записаться на курс", callback_data="manager"),
        ],

        [
            InlineKeyboardButton(text="️ В меню", callback_data="main_menu"),
        ]
    ]
)