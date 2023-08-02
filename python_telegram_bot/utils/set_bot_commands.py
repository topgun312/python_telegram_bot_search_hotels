from telebot import TeleBot
from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot: TeleBot) -> None:
    """
    Функция для установки стандартных команд бота.
    :param bot: телеграмм бот
    """
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )