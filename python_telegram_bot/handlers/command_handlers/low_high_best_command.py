from telebot.types import Message
from states.hotels_information import Hotel_priceInfo
from loader import bot
from telebot.types import ReplyKeyboardRemove
from keyboards.inline.location import city_markup
from keyboards.inline.end_result import count_hotels


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def user_query(message: Message) -> None:
    """
    Функция для получения и записи введенной команды в класс состояний пользователя.
    :param message: введенная пользователем команда
    """
    bot.set_state(message.from_user.id, Hotel_priceInfo.city, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['user_command'] = message.text
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, в каком городе ищем отель? 🗺', reply_markup=ReplyKeyboardRemove())


@bot.message_handler(state=Hotel_priceInfo.city)
def get_city(message: Message) -> None:
    """
    Функция для ввода города поиска вариантов размещения (отеля) и сохранение в класс состояний пользователя.
    :param message: введенный пользователем город поиска вариантов размещения (отеля)
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
        city_keyboard = city_markup(message.text)
        if city_keyboard:
            bot.send_message(message.from_user.id, 'Уточните пожалуйста локацию 📌', reply_markup=city_keyboard)
        else:
            bot.send_message(message.from_user.id, 'Город должен содержать только буквы!')


@bot.message_handler(state=Hotel_priceInfo.price_min)
def get_min_price(message: Message) -> None:
    """
    Функция получения минимальной цены за сутки от пользователя и сохранения в класс состояний пользователя.
    :param message: минимальная сумма за сутки, введенная пользователем.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data['user_command'] in ['/lowprice', '🔝 Дешевых отелей 🏠']:
            if message.text.isdigit():
                bot.send_message(message.from_user.id, 'Введите количество взрослых посетителей 👨🏻‍🦰')
                bot.set_state(message.from_user.id, Hotel_priceInfo.adults, message.chat.id)
                data['price_min'] = message.text
            else:
                bot.send_message(message.from_user.id, 'Цена должна быть числом!')
        elif data['user_command'] in [ '/bestdeal', '🔝 Наилучшее предложение 🏘']:
            if message.text.isdigit():
                bot.send_message(message.from_user.id, 'Введите максимальную цену за сутки ($) 💰')
                bot.set_state(message.from_user.id, Hotel_priceInfo.price_max, message.chat.id)
                data['price_min'] = message.text
            else:
                bot.send_message(message.from_user.id, 'Цена должна быть числом!')


@bot.message_handler(state=Hotel_priceInfo.price_max)
def get_max_price(message: Message) -> None:
    """
    Функция получения максимальной цены за сутки от пользователя и сохранения в класс состояний пользователя.
    :param message: максимальная сумма за сутки, введенная пользователем.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text.isdigit():
            bot.send_message(message.from_user.id, 'Введите количество взрослых посетителей 👨🏻‍🦰')
            bot.set_state(message.from_user.id, Hotel_priceInfo.adults, message.chat.id)
            data['price_max'] = message.text
        else:
            bot.send_message(message.from_user.id, 'Цена должна быть числом!')


@bot.message_handler(state=Hotel_priceInfo.adults)
def get_adults(message: Message) -> None:
    """
    Функция получения количества и возраста детей от пользователя и сохранения в класс состояний пользователя.
    :param message: количество и возраст детей, введенные пользователем.
    """
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Если с Вами дети, введите возраст каждого (до 18 лет) через запятую (Например (3-е детей): 3, 5, 6), иначе напишите "нет'' 👩🏻‍🦲')
        bot.set_state(message.from_user.id, Hotel_priceInfo.childrens, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['adults'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Цена должна быть числом!')



@bot.message_handler(state=Hotel_priceInfo.childrens)
def get_childrens(message: Message) -> None:
    """
    Функция получения количества и возраста детей пользователя.
    :param message: список количества детей и их возраст, введенный пользователем.
    """
    age_list = []
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            for s in message.text.split(','):
                age_list.append(s)
            if age_list[0] == 'нет':
                data['childrens'] = 0
                bot.send_message(message.from_user.id, 'Максимальное количество отелей для просмотра 🎲',
                                 reply_markup=count_hotels())
                bot.set_state(message.from_user.id, Hotel_priceInfo.hotels_count, message.chat.id)
            elif [s for s in age_list if s.isdigit()] and int(s) < 18:
                data['childrens'] = age_list
                bot.send_message(message.from_user.id, 'Максимальное количество отелей для просмотра 🎲',
                                 reply_markup=count_hotels())
                bot.set_state(message.from_user.id, Hotel_priceInfo.hotels_count, message.chat.id)
            else:
                    bot.send_message(message.from_user.id, 'Введите один из предложенных ответов!')