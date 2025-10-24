from aiogram import Router, types, Bot, F
from external_services.api_client_user import StudentAPI, GroupsAPI
from keyboards.inline_keyboards import get_main_menu,get_teacher_account,return_menu
import logging

profile_router = Router()
photo = types.FSInputFile("img.png")


def format_complete_student_info(student_data: dict, progress_data: dict = None) -> str:
    """Форматирует полную информацию о студенте в одном сообщении"""
    if not student_data:
        return "❌ Информация о студенте не найдена"

    full_name = student_data.get('full_name', 'Не указано')
    username = student_data.get('username', 'Не указан')
    group_title = student_data.get('group_title', 'Не указана')
    progress_level = student_data.get('progress_level', 'Новичок')
    is_active = student_data.get('is_active', True)
    average_score = student_data.get('average_score', 0.0)
    best_score = student_data.get('best_score', 0.0)
    total_points = student_data.get('total_points', 0.0)

    total_homeworks = student_data.get('total_homeworks', 0)
    completed_homeworks = student_data.get('completed_homeworks', 0)
    rank = student_data.get('rank', 0)

    progress_percent = 0
    if total_homeworks > 0:
        progress_percent = (completed_homeworks / total_homeworks) * 100

    def get_progress_bar(percentage, length=15):
        filled = int((percentage / 100) * length)
        empty = length - filled
        return "█" * filled + "░" * empty

    progress_bar = get_progress_bar(progress_percent)

    status_emoji = "✅" if is_active else "❌"

    complete_text = f"""
👤 <b>ПРОФИЛЬ СТУДЕНТА</b>

📝 <b>Личная информация:</b>
├ Имя: {full_name}
├ Username: @{username}
├ Группа: {group_title}
├ Уровень: {progress_level}
└ Статус: {status_emoji} {'Активен' if is_active else 'Неактивен'}

📊 <b>Учебный прогресс:</b>
├ Выполнено: {completed_homeworks}/{total_homeworks} заданий
├ Процент выполнения: {progress_percent:.1f}%
├ Прогресс: {progress_bar}
└ Рейтинг в academy: #{rank}

🎯 <b>Академические результаты:</b>
├ Средний балл: {average_score:.1f}
├ Лучший балл: {best_score:.1f}
└ Всего баллов: {total_points:.1f}

⭐ <b>Текущий статус:</b> {progress_level}
"""

    if progress_data:
        last_homework = progress_data.get('last_homework_done')
        if last_homework:
            complete_text += f"\n📅 <b>Последнее задание:</b> {last_homework}"

    return complete_text


@profile_router.callback_query(F.data == "menu:profile")
async def show_complete_profile(callback: types.CallbackQuery, bot: Bot):
    """Показывает полный профиль студента в одном сообщении"""
    user_telegram_id = str(callback.from_user.id)

    try:
        await callback.answer()

        async with StudentAPI() as student_api:
            student = await student_api.get_student_by_telegram_id(user_telegram_id)

            if not student:
                await callback.message.answer(
                    "❌ Профиль не найден. Используйте /start для регистрации в системе.",
                    reply_markup=return_menu()
                )
                return

            progress = await student_api.get_student_progress(user_telegram_id)

            profile_text = format_complete_student_info(student, progress)

            await callback.message.edit_caption(
                caption=profile_text,
                reply_markup=return_menu(),
                parse_mode="HTML"
            )

    except Exception as e:
        logging.error(f"Error showing complete profile: {e}")
        await callback.message.answer(
            "❌ Ошибка при загрузке профиля. Попробуйте позже.",
            reply_markup=return_menu()
        )


