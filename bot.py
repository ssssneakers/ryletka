import logging
import random
import telebot
from button import markup_game1, markup_menu, markup_choise1, markup_choise2, markup_game2
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
        # with open(bodya33, 'rb') as file:
        # bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, 'Привет! Я ботик созданный big cockом.Твой баланс равен 1000 шмеклей. Хочешь начать?\n'
                                          'Для начала этого нажми на кнопку "Инфа" и ознакомься с правилами.', reply_markup=markup_menu)

    else:
        # with open(bodya33, 'rb') as file:
        # bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, 'Здорова! Это мини казино от Лаптева.\n'
                                          'Перед тем чтобы начать играть лучше нажми на кнопку "Инфа" и ознакомься с правилами.\n'
                                          'Удачи!', reply_markup=markup_menu)
    save_data()


@bot.message_handler(func=lambda message: message.text == 'Балик')
def balance(message):
    user_id = message.from_user.id
    balance = user_balances[user_id]
    bot.send_message(message.chat.id, f"Ваш баланс: {balance}евродоллоров$")


@bot.message_handler(func=lambda message: message.text == 'Самые сладкие')
def leaderboard_handler(message):
    global leaderboard
    leaderboard = sorted(user_balances.items(), key=lambda x: x[1], reverse=True)
    leaders_str = "Топ 10 игроков:\n"
    for idx, (user_id, balance) in enumerate(leaderboard[:10], start=1):
        user_name = bot.get_chat(user_id).first_name
        leaders_str += f"{idx}. {user_name}: {balance} руб.\n"
    bot.send_message(message.chat.id, leaders_str)


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
        user_balances[user_id] -= 100  # Уменьшаем баланс на 100

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

    if random.randint(1, 6) == 1:
        # with open(grystni_grigos, 'rb') as file:
        # bot.send_photo(message.chat.id, file)
        user_balances[user_id] *= 2  # Увеличиваем баланс вдвое при выигрыше
        bot.send_message(message.chat.id, "Поздравляю! Вы победили и удвоили свой кэш.")

    else:
        # with open(happy_grigos, 'rb') as file:
        # bot.send_photo(message.chat.id, file)
        user_balances[user_id] = 0  # Обнуляем баланс при проигрыше
        bot.send_message(message.chat.id, "Лудоман иди работай!")

    bot.send_message(message.chat.id, f"Ваш текущий баланс: {user_balances[user_id]} евро", reply_markup=markup_game2)


@bot.message_handler(func=lambda message: message.text == 'Еще раз')
def restart_game(message):
    user_id = message.from_user.id
    in_game[user_id] = False
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "Давай сыграем еще раз!", reply_markup=markup_game1)
    game_kamen1(message)  # Вызов функции game_kamen для начала новой игры


@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.send_message(message.chat.id, 'Извините, я вас не понимаю. Выберите то что вам нужно.', reply_markup=markup_menu)
    bot.register_next_step_handler(message, back_to_menu)


bot.polling()
