import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
RAPID_API_HOST = os.getenv('RAPID_API_HOST')
DEFAULT_COMMANDS = (('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('lowprice', "Узнать топ самых дешёвых отелей в городе"),
    ('highprice', "Узнать топ самых дорогих отелей в городе"),
    ('bestdeal', "Узнать топ отелей, наиболее подходящих по цене " \
     "и расположению от центра (самые дешёвые и находятся ближе всего к центру)"))

ALL_STEPS = {'y': 'год 📆', 'm': 'месяц 📅', 'd': 'день 📅'}