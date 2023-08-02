from telebot.types import Message
from keyboards.reply.start_keyboard import markup_2, markup_3
from keyboards.reply.history_keyboard import markup_db
from database.sqlite_db import get_sql_db, delete_info
from loader import bot
from handlers.command_handlers.low_high_best_command import user_query
from config_data.config import DEFAULT_COMMANDS
from telebot.types import ReplyKeyboardRemove


@bot.message_handler(content_types=['text'])
def bot_message(message: Message) -> None:
    """
    Функция для начала поиска вариантов размещения (отелей).
    :param message: введенное пользователем сообщение.
    """
    if message.text == '🚀 Старт 🚀':
        bot.send_message(message.chat.id, 'Выберите для себя наилучшее предложение 👌', reply_markup=markup_2)
        bot.register_next_step_handler(message, bot_menu)


def bot_menu(message: Message) -> None:
    """
    Функция для выбора вариантов размещения (отеля), истории поиска и помощи при выборе.
    :param message: введенное пользователем сообщение.
    """
    if message.text == '🔝 Дешевых отелей 🏠' or message.text == '🔝 Дорогих отелей 🏡' or message.text == '🔝 Наилучшее предложение 🏘':
        user_query(message)

    elif message.text == '🔎 История поиска 📖':

        bot.send_message(message.chat.id, 'Нажмите на кнопки для просмотра или очистки истории поиска  📜', reply_markup=markup_db)
        bot.register_next_step_handler(message, bot_db)

    elif message.text == '🚨 Помощь 🚨':
        bot.send_message(message.from_user.id, 'Список команда нашего телеграм бота: 🗒 ', reply_markup=ReplyKeyboardRemove())
        text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
        bot.reply_to(message, '\n'.join(text))


def bot_db(message: Message) -> None:
    """
    Функция для работы с БД (просмотром и очисткой истории поиска вариантов размещения).
    :param message: введенное пользователем сообщение.
    """
    if message.text == '🕵🏻‍♂Показать историю поиска📜':
        history = get_sql_db()
        if history:
            for part in history:
                url = 'https://hotels.com/ho' + str(part[2])
                name = part[3]
                name_url = f'<a href="{url}">"{name}"</a> '

                history_info = f'Введенная команда: {part[0]} \n' + \
                                     f'Город поиска: {part[1]} \n' + \
                                     f'Название отеля: {name_url} \n' +\
                                     f'Дата и время поиска: {part[5]}'

                bot.send_photo(message.from_user.id, photo=(f'{part[4]}'), caption=history_info, parse_mode='html',reply_markup=markup_3)
            bot.register_next_step_handler(message, bot_back)

        else:
            bot.send_message(message.chat.id, 'История поиска пуста 💭', reply_markup=markup_3)
            bot.register_next_step_handler(message, bot_back)

    elif message.text == '🧹Очистить историю поиска🗑':
        delete_info()
        bot.send_message(message.chat.id, 'История поиска удалена 👌', reply_markup=markup_3)
        bot.register_next_step_handler(message, bot_back)


def bot_back(message: Message) -> None:
    """
    Функция выхода с истории поиска назад или в главное меню.
    :param message: введенное пользователем сообщение.
    """
    if message.text == '🔙 Назад 🔙':
        bot.send_message(message.chat.id, 'Выберите просмотр истории или удаление 👌', reply_markup=markup_db)
        bot.register_next_step_handler(message, bot_db)

    elif message.text == '🔙 В главное меню 🔙':
        bot.send_message(message.chat.id, 'Выберите для себя наилучшее предложение 👌', reply_markup=markup_2)
        bot.register_next_step_handler(message, bot_menu)