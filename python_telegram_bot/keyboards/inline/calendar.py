from telegram_bot_calendar import DetailedTelegramCalendar
from datetime import date, timedelta
from telebot.types import CallbackQuery
from states.hotels_information import Hotel_priceInfo
from loader import bot
from config_data.config import ALL_STEPS
from typing import Optional, Union


def get_calendar(is_process: Optional[bool] = False, callback_data: CallbackQuery = None, **kwargs) -> Union[tuple[date, str, str], tuple[str, str]]:
    """
    Функция для получения календаря при выборе даты заезда и выезда с отеля.
    :param is_process: состояние календаря.
    :param callback_data: информация из callback_data нажатой кнопки.
    :param kwargs: словарь значений календаря.
    :return: кортеж с результатами получения календаря.
    """
    if is_process:
        result, key, step = DetailedTelegramCalendar(calendar_id=kwargs['calendar_id'],
                                                     current_date=kwargs.get('current_date'),
                                                     min_date=kwargs['min_date'],
                                                     max_date=kwargs['max_date'],
                                                     locale=kwargs['locale']).process(callback_data.data)
        return result, key, step

    else:
        calendar, step = DetailedTelegramCalendar(calendar_id=kwargs['calendar_id'],
                                                  current_date=kwargs.get('current_date'),
                                                  min_date=kwargs['min_date'],
                                                  max_date=kwargs['max_date'],
                                                  locale=kwargs['locale']).build()
        return calendar, step


def calendar_process_first(call: CallbackQuery) -> None:
    """
    Функция выбора даты заезда в отель.
    :param call: выбор пользователя при нажатии на клавиатуру.
    """
    today = date.today()
    result, key, step = get_calendar(
        calendar_id=1,
        current_date=today,
        min_date=today,
        max_date=today + timedelta(days=548),
        locale='ru',
        is_process=True,
        callback_data=call
    )
    if not result and key:
        bot.edit_message_text(f"Выберите {ALL_STEPS[step]}",
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:

        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['check_in'] = result
        bot.delete_message(call.message.chat.id, call.message.message_id)

        calendar, step = get_calendar(calendar_id=2,
                                        min_date=result + timedelta(days=1),
                                        max_date=result + timedelta(days=548),
                                        locale="ru"
                                        )
        bot.send_message(call.from_user.id,
                         f"Выберите дату выезда ({ALL_STEPS[step]})",
                         reply_markup=calendar)


def calendar_process_second(call: CallbackQuery) -> None:
    """
    Функция для выбора даты выезда из отеля.
    :param call: выбор пользователя при нажатии на клавиатуру.
    """
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        date_check_in = data['check_in']
    result, key, step = get_calendar(
        calendar_id=2,
        current_date=date_check_in,
        min_date=date_check_in + timedelta(days=1),
        max_date=date_check_in + timedelta(days=548),
        locale='ru',
        is_process=True,
        callback_data=call
    )

    if not result and key:
        bot.edit_message_text(f"Выберите {ALL_STEPS[step]}",
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=key)

    elif result:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['check_out'] = result
        bot.delete_message(call.message.chat.id, call.message.message_id)

        if data['user_command'] in ['/lowprice', '🔝 Дешевых отелей 🏠', '/bestdeal', '🔝 Наилучшее предложение 🏘']:
            bot.send_message(call.from_user.id, 'Введите минимальную цену за сутки ($) 💰')
            bot.set_state(call.from_user.id, Hotel_priceInfo.price_min, call.message.chat.id)

        if data['user_command'] in ['/highprice', '🔝 Дорогих отелей 🏡']:
            bot.send_message(call.from_user.id, 'Введите максимальную цену за сутки ($) 💰')
            bot.set_state(call.from_user.id, Hotel_priceInfo.price_max, call.message.chat.id)