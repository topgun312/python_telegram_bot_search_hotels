from telebot.types import Message
from keyboards.reply.start_keyboard import markup_1
from loader import bot
from config_data.config import DEFAULT_COMMANDS


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Стартовая функция для начала работы бота.
    :param message: введеная команда пользователем.
    """
    bot.send_message(message.chat.id, f"Здравствуйте ✌ {message.from_user.first_name}, "
                          f" если Вы ищите лучшее предложение по отелям нажмите '🚀 Старт 🚀'!", reply_markup=markup_1)


@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    """
    Функция для работы команды help.
    :param message: введенная команда пользователем.
    """
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.chat.id, '\n'.join(text))