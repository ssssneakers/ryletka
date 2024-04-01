import logging
import random
import telebot
from button import markup_game1, markup_menu, markup_choise1, markup_choise2, markup_game2, markup_info
from config import token
import json
from photo import bodya33, grystni_grigos, happy_grigos

bot = telebot.TeleBot(token)

logging.basicConfig(filename='errors.cod.log', level=logging.ERROR, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

# Таблица лидеров
in_game = {}


# Загружаем данные из файла
def load_data():
    try:
        with open('user_balances.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


user_balances = load_data()

# Таблица лидеров
leaderboard = []


def save_data():
    with open('user_balances.json', 'w') as file:
        json.dump(user_balances, file, indent=4)

    with open('leaderboard.json', 'w') as file:
        json.dump(leaderboard, file, indent=4)


@bot.message_handler(commands=['debug'])
def debug(message):
    with open('errors.cod.log', 'rb') as file:
        bot.send_document(message.chat.id, file)


@bot.message_handler(func=lambda message: message.text == 'Поддержка')
def support(message):
    bot.send_message(message.chat.id, 'Для связи с поддержкой пишите нашему администратору в телегу:https://t.me/Programist337')


@bot.message_handler(func=lambda message: message.text == 'Вернуться в меню')
def back_to_menu(message):
    user_id = message.from_user.id
    in_game[user_id] = False
    bot.send_message(message.chat.id, 'Возвращаю в меню ', reply_markup=markup_menu)
    save_data()


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    in_game[user_id] = False
    if user_id not in user_balances:  # Проверяем, есть ли пользователь в базе
        user_balances[user_id] = 1000
        with open(bodya33, 'rb') as file:
            bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, 'Привет! Я ботик созданный big cockом.Твой баланс равен 1000 шмеклей. Хочешь начать?\n'
                                          'Для начала этого нажми на кнопку "Инфа" и ознакомься с правилами.', reply_markup=markup_menu)

    else:
        with open(bodya33, 'rb') as file:
            bot.send_photo(message.chat.id, file)
            bot.send_message(message.chat.id, 'Здорова! Это мини казино от Лаптева.\n'
                                              'Перед тем чтобы начать играть лучше нажми на кнопку "Инфа" и ознакомься с правилами.\n'
                                              'Удачи!', reply_markup=markup_menu)
    save_data()


@bot.message_handler(func=lambda message: message.text == 'Самые сладкие')
def leaderboard_handler(message):
    global leaderboard
    leaderboard = sorted(user_balances.items(), key=lambda x: x[1], reverse=True)

    # Находим место пользователя в топе
    user_id = message.from_user.id
    user_balance = user_balances.get(user_id, 0)
    user_place = next((idx + 1 for idx, (id, _) in enumerate(leaderboard) if id == user_id), None)

    if user_place:
        user_place_str = f"Ваше место в топе: {user_place}\n"
    else:
        leaderboard.append((user_id, user_balance))  # Добавляем пользователя в таблицу лидеров
        leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)
        user_place = next(idx + 1 for idx, (id, _) in enumerate(leaderboard) if id == user_id)
        user_place_str = f"Ваше место в топе: {user_place}\n"

    bot.send_message(message.chat.id, user_place_str)

    # Отправляем топ лидеров
    leaders_str = "Топ 10 игроков:\n"
    for idx, (user_id, balance) in enumerate(leaderboard[:10], start=1):
        user_name = bot.get_chat(user_id).first_name
        leaders_str += f"{idx}. {user_name}: {balance} руб.\n"

    bot.send_message(message.chat.id, leaders_str)


@bot.message_handler(func=lambda message: message.text == 'Инфа')
def info(message):
    bot.send_message(message.chat.id, 'Здорова! Если вкратце об function бота \n'
                                      'При запуске бота вас встретит меню со следующим набором кнопок\n'
                                      '"Начнем возню"- открывает меню с списком всех игр\n'
                                      '"Напивкокенту!"- позволяет большому папочке радовать своего бомже друга\n'
                                      '"Самые сладкие"- это что то вроде таблицы лидеров.Она показывает твой баланс и позицию в топе на которой ты находишься\n'
                                      '"Поддержка"- ну тут указаны мои цифры для связи\n'
                                      'Быть добру!', reply_markup=markup_info)


# Функция для перевода валюты
#@bot.message_handler(func=lambda message: message.text == 'Напивкокенту!')
def send_money(message):
    bot.send_message(message.chat.id, "для начала выбери кентa, возьми его ID(в формате @username) и подумай над суммой перевода.\n"
                                      "Когда решишься отправляй сообщение в формате: /перевод @получатель сумма", reply_markup=markup_choise2)

    bot.register_next_step_handler(message, transfer_money)


def transfer_money(message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.send_message(message.chat.id, "Некорректный формат. Используйте: /перевод @получатель сумма")
            return

        receiver = parts[1]
        amount = int(parts[2])
        sender_id = message.from_user.id

        if amount <= 0:
            bot.send_message(message.chat.id, "Сумма должна быть положительным числом.")
            return

        if sender_id not in user_balances:
            bot.send_message(message.chat.id, "У вас нет средств для перевода.")
            return

        if user_balances[sender_id] < amount:
            bot.send_message(message.chat.id, "У вас недостаточно средств для перевода этой суммы.")
            return

        if receiver in user_balances:
            user_balances[sender_id] -= amount
            user_balances[receiver] += amount
            if user_balances[sender_id] < 0:
                user_balances[sender_id] += amount  # Откатываем изменение баланса отправителя
                bot.send_message(message.chat.id, "У вас недостаточно средств для перевода этой суммы.")
            else:
                save_data()
                bot.send_message(message.chat.id, f"Вы успешно перевели {amount} пользователю {receiver}.")
        else:
            bot.send_message(message.chat.id, "Получатель не найден в базе данных.")

    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Некорректный формат. Используйте: /перевод @получатель сумма")


@bot.message_handler(func=lambda message: message.text == 'Начнем возню')
def start_game(message):
    user_id = message.from_user.id
    balance = user_balances[user_id]
    bot.send_message(message.chat.id, f"Напомню, что твой баланс равен: {balance}рупий.\n"
                                      f"Теперь выбери игру.", reply_markup=markup_choise1)


@bot.message_handler(func=lambda message: message.text == 'Камень,Ножницы,Бумага')
def game_kamen1(message):
    user_id = message.from_user.id
    if in_game[user_id] == True:  # Проверяем, идет ли уже игра
        bot.send_message(message.chat.id, "Игра уже начата. Завершите текущую игру или выберите 'Еще раз'.")
        return

    in_game[user_id] = True
    bot.send_message(message.chat.id, 'Делай свой выбор,боров', reply_markup=markup_game1)
    bot.register_next_step_handler(message, game_kamen)


def game_kamen(message):
    user_id = message.from_user.id
    choices = ['Камень', 'Ножницы', 'Бумага']
    user_choice = message.text
    bot_choice = random.choice(choices)
    result = ''

    if user_choice == bot_choice:
        result = 'Ничья!'

    elif (user_choice == 'Камень' and bot_choice == 'Ножницы') or \
            (user_choice == 'Ножницы' and bot_choice == 'Бумага') or \
            (user_choice == 'Бумага' and bot_choice == 'Камень'):
        result = 'Ты победил!'
        user_balances[user_id] += 100  # Увеличиваем баланс на 100
    else:
        result = 'Ты проиграл!'

    in_game[user_id] = False
    bot.send_message(message.chat.id, f"Твой выбор: {user_choice}\n"
                                      f"Выбор бота: {bot_choice}\n"
                                      f"Результат: {result}\n"
                                      f"Баланс: {user_balances[user_id]}$", reply_markup=markup_choise2)


@bot.message_handler(func=lambda message: message.text == 'Русская рулетка')
def russian_roulette_game(message):
    user_id = message.from_user.id
    if in_game[user_id]:  # Проверяем, идет ли уже игра
        bot.send_message(message.chat.id, "Игра уже начата. Завершите текущую игру или выберите 'Еще раз'.")
        return

    in_game[user_id] = True
    bot.send_message(message.chat.id, 'Ну что, боров, крути барабан', reply_markup=markup_game2)


@bot.message_handler(func=lambda message: message.text == 'Крутить барабан')
def russian_roulette(message):
    user_id = message.from_user.id
    balance = user_balances[user_id]
    if balance <= 0:
        bot.send_message(message.chat.id, "У вас недостаточно мани для игры.")
        return

    if random.randint(1, 12) == 1:
        with open(grystni_grigos, 'rb') as file:
            bot.send_photo(message.chat.id, file)
        user_balances[user_id] *= 2  # Увеличиваем баланс вдвое при выигрыше
        bot.send_message(message.chat.id, "Поздравляю! Вы победили и удвоили свой кэш.")
    else:
        with open(happy_grigos, 'rb') as file:
            bot.send_photo(message.chat.id, file)
        user_balances[user_id] = 0  # Обнуляем баланс при проигрыше
        bot.send_message(message.chat.id, "Лудоман иди работай!")

    bot.send_message(message.chat.id, f"Ваш текущий баланс: {user_balances[user_id]} евро", reply_markup=markup_game2)


@bot.message_handler(func=lambda message: message.text == 'Еще раз')
def restart_game(message):
    user_id = message.from_user.id
    in_game[user_id] = False
    bot.send_message(message.chat.id, "Давай сыграем еще раз!", reply_markup=markup_game1)
    game_kamen1(message)  # Вызов функции game_kamen для начала новой игры


@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.send_message(message.chat.id, 'Извините, я вас не понимаю. Выберите то что вам нужно.', reply_markup=markup_menu)
    bot.register_next_step_handler(message, back_to_menu)


bot.polling()
