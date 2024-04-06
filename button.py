from telebot import types

# Кнопки для главного меню
markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_menu.add(types.KeyboardButton('Инфа'))
markup_menu.add(types.KeyboardButton('Начнем возню'))
markup_menu.add(types.KeyboardButton('Напивкокенту!'))
markup_menu.add(types.KeyboardButton('Самые сладкие'))
markup_menu.add(types.KeyboardButton('Поддержка'))
markup_menu.add(types.KeyboardButton('Узнать ID'))
markup_menu.add(types.KeyboardButton('Crypto'))

# Кнопки для выбора игры
markup_choise1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_choise1.add(types.KeyboardButton('Вернуться в меню'))
markup_choise1.add(types.KeyboardButton('Камень,Ножницы,Бумага'))
markup_choise1.add(types.KeyboardButton('Русская рулетка'))
markup_choise1.add(types.KeyboardButton('Слоты'))

# Кнопки после завершения игры
markup_choise2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_choise2.add(types.KeyboardButton('Еще раз'))
markup_choise2.add(types.KeyboardButton('Вернуться в меню'))

# Кнопка для игры в камень-ножницы-бумага
markup_game1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_game1.add(types.KeyboardButton('Камень'))
markup_game1.add(types.KeyboardButton('Ножницы'))
markup_game1.add(types.KeyboardButton('Бумага'))

# Кнопка для игры в русскую рулетку
markup_game2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_game2.add(types.KeyboardButton('Крутить барабан'))
markup_game2.add(types.KeyboardButton('Вернуться в меню'))


# Кнопка для инфы
markup_info = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_info.add(types.KeyboardButton('Вернуться в меню'))

# Кнопка для криптовалют
markup_crypto = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_crypto.add(types.KeyboardButton('Топ крипт'))
markup_crypto.add(types.KeyboardButton('Стать трейдером'))
markup_crypto.add(types.KeyboardButton('Create Crypto'))
markup_crypto.add(types.KeyboardButton('Моя крипта'))
markup_crypto.add(types.KeyboardButton('Вернуться в меню'))
