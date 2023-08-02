from loader import bot
from keyboards.inline import location, calendar, end_result
from telegram_bot_calendar import DetailedTelegramCalendar


def register_handler() -> None:
    """
    Функция для регистрации всех коллбэк хэндлеров инлайн клавиатуры.
    """
    bot.register_callback_query_handler(location.answer_loc, func=lambda call: call.data.startswith('destination'))
    bot.register_callback_query_handler(calendar.calendar_process_first, func=DetailedTelegramCalendar.func(calendar_id=1))
    bot.register_callback_query_handler(calendar.calendar_process_second, func=DetailedTelegramCalendar.func(calendar_id=2))
    bot.register_callback_query_handler(end_result.answer, func=lambda call: call.data.startswith('hotels_count'))
    bot.register_callback_query_handler(end_result.send_photo, func=lambda call: call.data.startswith('id'))
    bot.register_callback_query_handler(end_result.close_message, lambda call: call.data == 'back')
    bot.register_callback_query_handler(end_result.show_hotel_photo, func=lambda call: call.data.split('#')[0] == 'picture')