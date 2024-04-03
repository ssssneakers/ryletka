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
    if user_id not in user_balances:  # Проверяем, есть ли пользователь в баgit add .зе
        user_balances[user_id] = 1000
        with open(bodya33, 'rb') as file:
            bot.send_photo(message.chat.id, file)
        bot.send_message(message.chat.id, 'Привет! Я ботик созданный big cockом.Твой баланс равен 1000 шмеклей. Хочешь начать?\n'
                                          'Для начала этого нажми на кнопку "Инфа" и ознакомься с правилами.', reply_markup=markup_menu)

    else:
        # with open(bodya33, 'rb') as file:
        # bot.send_photo(message.chat.id, file)
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
                                      'Важно!Если что то не работает, то начните с команды старт и попробуйте ещё раз\n'
                                      'Если что пишите мне на телегу @Programist337 \n'
                                      'При запуске бота вас встретит меню со следующим набором кнопок\n'
                                      '"Начнем возню"- открывает меню с списком всех игр\n'
                                      '"Напивкокенту!"- позволяет большому папочке радовать своего бомже друга(самая жесткая функция в данном боте)\n'
                                      '"Самые сладкие"- это что то вроде таблицы лидеров.Она показывает твой баланс и позицию в топе на которой ты находишься\n'
                                      '"Поддержка"- ну тут указаны мои цифры для связи\n'
                                      '"Узнать ID"- показывает твой ID\n'
                                      'Быть добру!', reply_markup=markup_info)


@bot.message_handler(func=lambda message: message.text == 'Узнать ID')
def user_ID(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, f"Твой ID: {user_id}", reply_markup=markup_info)


# Функция для перевода валюты
@bot.message_handler(func=lambda message: message.text == 'Напивкокенту!')
def send_money(message):
    bot.send_message(message.chat.id, "для начала выбери кентa, попроси его ID и подумай над суммой перевода.\n"
                                      "Когда решишься отправляй сообщение в формате(если выбираешь анон то сообщение старайся писать без пробелов): /перевод получатель сумма [анон]/[] сообщение\n"
                                      "Например: /перевод 5456456456 999 [анон] От Шмелека!", reply_markup=markup_info)

    bot.register_next_step_handler(message, transfer_money)


def transfer_money(message):
    try:
        parts = message.text.split(maxsplit=4)
        if len(parts) < 4:
            bot.send_message(message.chat.id, "Некорректный формат. Используйте: /перевод @получатель сумма [анон] сообщение")
            return

        receiver_username = parts[1]
        amount = int(parts[2])
        sender_id = message.from_user.id
        is_anonymous = False
        message_text = ' '.join(parts[4:])

        if parts[3].lower() == "анон":
            is_anonymous = True

        if amount <= 0:
            bot.send_message(message.chat.id, "Сумма должна быть положительным числом.")
            return

        sender_balance = user_balances.get(sender_id)
        if sender_balance is None:
            bot.send_message(message.chat.id, "У вас нет средств для перевода.")
            return

        if sender_balance < amount:
            bot.send_message(message.chat.id, "У вас недостаточно средств для перевода этой суммы.")
            return

        if receiver_username not in user_balances:
            bot.send_message(message.chat.id, "Пользователь не найден.")
            return

        sender_balance -= amount
        receiver_balance = user_balances[receiver_username]
        receiver_balance += amount

        user_balances[sender_id] = sender_balance
        user_balances[receiver_username] = receiver_balance

        bot.send_message(message.chat.id, f"Перевод успешно выполнен! Вы отправили {amount} руб. пользователю {receiver_username}.")

        receiver_id = bot.get_chat(receiver_username).id
        if is_anonymous:
            bot.send_message(receiver_id, f"Вам был отправлен анонимный перевод в размере {amount} руб.")
        else:
            bot.send_message(receiver_id, f"Вам был отправлен перевод в размере {amount} руб. от пользователя {message.from_user.username}.\nСообщение: {message_text}")

    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Некорректный формат. Используйте: /перевод @получатель сумма [анонимно] сообщение")


@bot.message_handler(func=lambda message: message.text == 'Начнем возню')
def start_game(message):
    user_id = message.from_user.id
    balance = user_balances[user_id]
    if user_id not in user_balances:
        user_balances[user_id] = 1000
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


@bot.message_handler(func=lambda message: message.text == 'Слоты')
def slots_game(message):
    user_id = message.from_user.id
    if in_game[user_id]:  # Проверяем, идет ли уже игра
        bot.send_message(message.chat.id, "Игра уже начата. Завершите текущую игру или выберите 'Еще раз'.")
        return

    in_game[user_id] = True
    bot.send_message(message.chat.id, 'Ну что, боров, ДЕЛАЙ СТАВКУ ЦИФРАМИ!!! (если хочешь сыграть еще раз просто напиши еще раз ставку)\n'
                                      'Чтобы выйти нажми вернуться в меню 2 раза', reply_markup=markup_info)

    bot.register_next_step_handler(message, play_slots)


def play_slots(message):
    user_id = message.from_user.id
    balance = user_balances[user_id]
    bet = message.text

    if not bet.isdigit():
        bot.send_message(message.chat.id, "Некорректная ставка. Введите число.")
        return

    bet = int(message.text)

    if bet > balance:
        bot.send_message(message.chat.id, "Куда ты, бомжик?")
        return

    if bet <= 0:
        bot.send_message(message.chat.id, "Некорректная ставка.")
        return

    symbols = ['💎', '🍀', '🍒', '🔔', '🍊', '🍇', '🌟', '777', '🍒🍒🍒']  # Символы для слотов
    reels = [random.choice(symbols) for _ in range(3)]  # Генерация символов на барабанах

    payout_table = {
        '777': 17 * bet,
        '🍒🍒🍒': 10 * bet,
        '💎💎💎': 9 * bet,
        '🍀🍀🍀': 6 * bet,
        '🔔🔔🔔': 5 * bet,
        '🍊🍊🍊': 2 * bet,
        '🍇🍇🍇': 2 * bet,
        '🌟🌟🌟': 2 * bet
    }  # Таблица выплат

    winning_symbol = reels[0]
    payout = payout_table.get(winning_symbol, 0)
    balance -= bet
    balance += payout
    reels_str = ' '.join(reels)

    if payout > 0:
        bot.send_message(message.chat.id, f"{reels_str}")
        bot.send_message(message.chat.id, f"УРАААА!!!!+{payout} руб.")
        bot.register_next_step_handler(message, play_slots)
    else:
        bot.send_message(message.chat.id, f"{reels_str}")
        bot.send_message(message.chat.id, "Вы проиграли.")
        bot.register_next_step_handler(message, play_slots)

    return reels, payout, balance


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
