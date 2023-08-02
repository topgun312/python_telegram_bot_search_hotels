from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from botrequest.rapidapi_copy import search_location
from loader import bot
from keyboards.inline.calendar import get_calendar
from config_data.config import ALL_STEPS
from datetime import date, timedelta


def city_markup(message: str) -> InlineKeyboardMarkup:
    """
    Функция для поиска локации вариантов размещения(отелей) и создания инлайн-клавиатуры с результатами поиска.
    :param message: введеное пользователем название города.
    :return: инлайн - клавиатура с локацией.
    """
    cities = search_location(message)
    if cities:
        destinations = InlineKeyboardMarkup()
        for city in cities:
            destinations.add(InlineKeyboardButton(text=city['city_name'],
                                                  callback_data=f'destination:{city["destination_id"]}'))
        return destinations


def answer_loc(call: CallbackQuery) -> None:
    """
    Функция для выбора пользователем локации вариантов размещения(отеля) и сохранения данных  в машину состояния.
    :param call: выбор пользователя при нажатии на клавиатуру.
    """
    if call.message:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['location'] = call.data.split(":")[1]

            for keyboard in call.message.reply_markup.keyboard:
                for i in keyboard:
                    if i.callback_data == call.data:
                        data['city_loc'] = i.text

        today = date.today()
        calendar, step = get_calendar(calendar_id=1,
                                      current_date=today,
                                      min_date=today,
                                      max_date=today + timedelta(days=365),
                                      locale="ru")
        bot.send_message(call.from_user.id, f"Выберите дату заезда ({ALL_STEPS[step]})", reply_markup=calendar)
        bot.delete_message(call.message.chat.id, call.message.message_id)