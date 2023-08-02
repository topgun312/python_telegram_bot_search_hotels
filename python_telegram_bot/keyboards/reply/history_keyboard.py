from telebot.types import ReplyKeyboardMarkup, KeyboardButton


markup_db = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_1 = KeyboardButton('🕵🏻‍♂Показать историю поиска📜')
keyboard_2 = KeyboardButton('🧹Очистить историю поиска🗑')
markup_db.add(keyboard_1, keyboard_2)