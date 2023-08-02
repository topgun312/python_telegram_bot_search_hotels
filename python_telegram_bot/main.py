from loader import bot
from telebot.custom_filters import StateFilter
from utils.set_bot_commands import set_default_commands
import handlers
from handlers.register_handlers.reg_handler import register_handler
from database.sqlite_db import sql_start
from loguru import logger


if __name__ == '__main__':
    sql_start()
    register_handler()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    logger.add("logs/logs_{time}.log", format="{time} {level} {message}", level="DEBUG", rotation="08:00", compression="zip")
    logger.debug('Error')
    logger.info('Information message')
    logger.warning('Warning')
    bot.infinity_polling()