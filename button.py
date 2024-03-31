from telebot import types

# Кнопки для главного меню
markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_menu.add(types.KeyboardButton('Инфа'))
markup_menu.add(types.KeyboardButton('Начнем возню'))
markup_menu.add(types.KeyboardButton('Балик'))
markup_menu.add(types.KeyboardButton('Самые сладкие'))
markup_menu.add(types.KeyboardButton('Поддержка'))

# Кнопки для выбора игры
markup_choise1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_choise1.add(types.KeyboardButton('Вернуться в меню'))
markup_choise1.add(types.KeyboardButton('Камень,Ножницы,Бумага'))
markup_choise1.add(types.KeyboardButton('Русская рулетка'))

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