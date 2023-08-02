import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, CallbackQuery, Message
from telebot import types
from loader import bot
from keyboards.reply.start_keyboard import markup_1
from botrequest import rapidapi_copy
from telegram_bot_pagination import InlineKeyboardPaginator
from states.hotels_information import Hotel_priceInfo
from database.sqlite_db import sql_add_command
from typing import Optional, Any, List


def count_hotels() -> InlineKeyboardMarkup:
    """
    Функция выбора количества вариантов размещения (отелей) для просмотра.
    :return: клавиатура для выбора количества отелей
    """
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    item_1 = InlineKeyboardButton(text='3 🏠', callback_data='hotels_count: 3')
    item_2 = InlineKeyboardButton(text='6 🏠', callback_data='hotels_count: 6')
    item_3 = InlineKeyboardButton(text='9 🏠', callback_data='hotels_count: 9')
    item_4 = InlineKeyboardButton(text='12 🏠', callback_data='hotels_count: 12')
    item_5 = InlineKeyboardButton(text='15 🏠', callback_data='hotels_count: 15')
    item_6 = InlineKeyboardButton(text='Все 🏘', callback_data='hotels_count: 25')
    markup_inline.add(item_1, item_2, item_3, item_4, item_5, item_6)
    return markup_inline


def answer(call: CallbackQuery) -> int:
    """
    Функция для вывода полной информации о результатах поиска вариантов размещения (отеля).
    :param call: выбор пользователем количества отелей для поиска
    :return: вывод количества отелей для просмотра.
    """
    if call.message:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['hotels_count'] = call.data.split(":")[1]
            hotels = call.data.split(':')[1]

            data_1 = str(data["check_in"]).split('-')
            data_2 = str(data["check_out"]).split('-')
            d_1 = datetime.date(int(data_1[0]), int(data_1[1]), int(data_1[2]))
            d_2 = datetime.date(int(data_2[0]), int(data_2[1]), int(data_2[2]))
            days = d_2 - d_1
            dd = str(days)
            period = dd.split()[0]

            if data['user_command'] in ['/lowprice', '🔝 Дешевых отелей 🏠', '/highprice', '🔝 Дорогих отелей 🏡']:
                text_low_high = f'<b>Параметры запроса.</b> \nГород поиска 🗺: {data["city_loc"]} \n' + \
                       f'Количество отелей 🎲: {hotels} \n' + \
                       f'Въезд ➡: {data["check_in"]} \n' + \
                       f'Выезд ⬅: {data["check_out"]} \n' + \
                       f'Веду поиск...🕵🏻‍♂'
                bot.send_message(call.message.chat.id, text_low_high, reply_markup=markup_1, parse_mode='html')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                hotels_info = rapidapi_copy.search_hotels(data)

            elif data['user_command'] in ['/bestdeal', '🔝 Наилучшее предложение 🏘']:
                text_bst = f'<b>Параметры запроса.</b> \nГород поиска 🗺: {data["city_loc"]} \n' + \
                           f'Количество отелей 🎲: {data["hotels_count"]} \n' + \
                           f'Въезд ➡: {data["check_in"]} \n' + \
                           f'Выезд ⬅: {data["check_out"]} \n' + \
                           f'Минимальная цена ⬇: {data["price_min"]} \n' + \
                           f'Максимальная цена ⬆: {data["price_max"]} \n' + \
                           f'Веду поиск...🕵🏻‍♂'
                bot.send_message(call.message.chat.id, text_bst, reply_markup=markup_1, parse_mode='html')
                bot.delete_message(call.message.chat.id, call.message.message_id)
                hotels_info = rapidapi_copy.search_hotels(data)

            for hotel in hotels_info.values():
                info = f' \nНаименование отеля 🏨: {hotel["name"]} \n' + \
                       f'Местоположение отеля 📪: {hotel["loc"]} \n' + \
                       f'Рейтинг отеля 🏆: {hotel["reviews"]} \n' + \
                       f'Расстояние от центра города 🚕: {round(hotel["landmarks"] * 1.61, 1)} км \n' + \
                       f'Цена за сутки 💳: {hotel["price"]} $\n' + \
                       f'Цена за период проживания 💰: {int(hotel["price"]) * int(period)} $'
                bot.send_photo(call.message.chat.id, photo=(f'{hotel["fonfoto"]}'), caption=info,
                               reply_markup=low_high_best_inline(hotel))
                date_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                message_db = [data['user_command'], data['city_loc'], hotel['id'], hotel['name'], hotel['fonfoto'],
                              date_time]
                sql_add_command(message_db)

            return hotel


def low_high_best_inline(hotel: int) -> InlineKeyboardMarkup:
    """
    Функция для создания инлайн - клавиатуры с локациией, ссылкой на отель, фотографиями отеля.
    :param hotel: количество отелей выбранных пользователем.
    :return: вывод инлайн - клавиатуры
    """
    markup = types.InlineKeyboardMarkup(row_width=1)
    item_1 = types.InlineKeyboardButton(text='🌍  На Google Maps 📌', url=f'http://maps.google.com/maps?z=12&t=m&q=loc:{hotel["coordinate"]}')
    item_2 = types.InlineKeyboardButton(text='🌐 На страницу 📲', url=f'https://www.hotels.com/h{hotel["id"]}.Hotel-information/')
    item_3 = types.InlineKeyboardButton(text='📸 Фотографии 🏙', callback_data=f'id:{hotel["id"]}')
    markup.add(item_1, item_2, item_3)
    return markup


def send_photo(call: CallbackQuery) -> Optional[list]:
    """
    Функция запроса поиска фото вариантов размещения (отеля) для создания пагинатора.
    :param call: выбор пользователя при нажатии на клавиатуру.
    :return: список url-адресов фото варианта размещения (отеля).
    """
    if call.message:
        id_hotel = call.data.split(':')[1]
        images = rapidapi_copy.search_photo_hotel(id_hotel)
        bot.set_state(call.message.from_user.id, Hotel_priceInfo.images, call.message.chat.id)
        with bot.retrieve_data(call.message.from_user.id, call.message.chat.id) as data:
            data['images'] = images
        bot.send_photo(call.message.chat.id, data['images'][0], reply_markup=create_photos_keyboard(len(data['images'])), parse_mode='Markdown')
        return images


def create_photos_keyboard(photos_amount: Any, page: int = 1) -> InlineKeyboardMarkup:
    """
    Функция создания инлайн - клавиатуры пагинатора.
    :param photos_amount: количество фотограций найденных в результате запроса.
    :param page: начальная цифра для отсчета при создании инлайн - клавиатуры.
    :return: инлайн - клавиатура.
    """
    paginator = InlineKeyboardPaginator(photos_amount, current_page=page, data_pattern='picture#{page}')
    paginator.add_after(InlineKeyboardButton('Закрыть ❌ ', callback_data='back'))
    return paginator.markup


def close_message(call: CallbackQuery) -> None:
    """
    Функция закрытия просмотра фотографий с пагинатора.
    :param call: выбор пользователя при нажатии на клавиатуру.
    """
    bot.delete_message(call.message.chat.id, call.message.message_id)


def show_hotel_photo(call: CallbackQuery) -> None:
    """
    Функция для просмотра фотографий в пагинаторе.
    :param call: выбор пользователя при нажатии на клавиатуру.
    """
    photo_index = int(call.data.split('#')[1])
    with bot.retrieve_data(call.message.from_user.id, call.message.chat.id) as data:
        photos = data['images']

    send_new_hotel_photo(message=call.message, found_photos=photos, photo_index=photo_index)


def send_new_hotel_photo(message: Message, found_photos: List[str], photo_index: int = 1) -> None:
    """
    Функция для переключения пагинатора для просмотра новой фотографии.
    :param message: сообщение введенное пользователем.
    :param found_photos: список фотографий для просмотра.
    :param photo_index: номер фотографии для просмотра.
    """
    bot.edit_message_media(chat_id=message.chat.id,
                               message_id=message.message_id,
                               media=InputMediaPhoto(found_photos[photo_index - 1]),
                               reply_markup=create_photos_keyboard(len(found_photos), page=photo_index))