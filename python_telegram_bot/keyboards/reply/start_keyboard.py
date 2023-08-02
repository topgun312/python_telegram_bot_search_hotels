from telebot.types import ReplyKeyboardMarkup, KeyboardButton


markup_1 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_1 = KeyboardButton('🚀 Старт 🚀')
markup_1.add(keyboard_1)


markup_2 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_1 = KeyboardButton('🔝 Дешевых отелей 🏠')
keyboard_2 = KeyboardButton('🔝 Дорогих отелей 🏡')
keyboard_3 = KeyboardButton('🔝 Наилучшее предложение 🏘')
keyboard_4 = KeyboardButton('🔎 История поиска 📖')
keyboard_5 = KeyboardButton('🚨 Помощь 🚨')
markup_2.add(keyboard_1, keyboard_2, keyboard_3, keyboard_4, keyboard_5)


markup_3 = ReplyKeyboardMarkup(resize_keyboard=True)
back = KeyboardButton('🔙 Назад 🔙')
back_menu = KeyboardButton('🔙 В главное меню 🔙')
markup_3.add(back, back_menu)
