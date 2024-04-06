import logging
import random
import telebot
from button import markup_game1, markup_menu, markup_choise1, markup_choise2, markup_game2, markup_info, markup_crypto
from config import token
import json
from photo import bodya33, grystni_grigos, happy_grigos

bot = telebot.TeleBot(token)

logging.basicConfig(filename='errors.cod.log', level=logging.ERROR, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

# Таблица лидеров
in_game = {}

user_balances = {}

leaderboard = []


# Загружаем данные из файла
def load_data():
    try:
        with open('user_balances.json', 'r', encoding='utf-8') as file:
            data = file.read()
            if not data:
                return {}  # Возвращаем пустой словарь, если файл пуст
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Загружаем криптовалюты
def crypto_data():
    try:
        with open('user_crypto.json', 'r', encoding='utf-8') as file:
            data = file.read()
            if not data:
                return {}  # Возвращаем пустой словарь, если файл пуст
            return json.loads(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_cryptocurrencies():
    try:
        with open('cryptocurrencies.json', 'r', encoding='utf-8') as file:
            data = file.read()
            if not data:
                return {}  # Возвращаем пустой словарь, если файл пуст
            return json.loads(data)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Обработка ошибок при отсутствии файла или некорректном JSON


try:
    cryptocurrencies = load_cryptocurrencies()
    user_balances = load_data()
    crypto_data = crypto_data()
except FileNotFoundError:
    cryptocurrencies = {}
    user_balances = {}
    crypto_data = {}


# Таблица лидеров


def save_cryptocurrencies(cryptocurrencies):
    try:
        with open('cryptocurrencies.json', 'w') as file:
            json.dump(cryptocurrencies, file, indent=4)
    except FileNotFoundError:
        return


def save_data():
    with open('user_balances.json', 'w') as file:
        json.dump(user_balances, file, indent=4)

    with open('leaderboard.json', 'w') as file:
        json.dump(leaderboard, file, indent=4)


def save_crypto_data():
    try:
        with open('user_crypto.json', 'w', encoding='utf-8') as file:
            json.dump(crypto_data, file, indent=4)
    except FileNotFoundError:
        return


@bot.message_handler(commands=['debug'])
def debug(message):
    with open('errors.cod.log', 'rb') as file:
        bot.send_document(message.chat.id, file)


@bot.message_handler(func=lambda message: message.text == 'Поддержка')
def support(message):
    bot.send_message(message.chat.id, 'Для связи с поддержкой пишите нашему администратору в телегу:https://t.me/Programist337')


@bot.message_handler(func=lambda message: message.text == 'Вернуться в меню')
def back_to_menu(message):
    user_id = message.from_user.username
    in_game[user_id] = False
    bot.send_message(message.chat.id, 'Возвращаю в меню ', reply_markup=markup_menu)
    save_data()


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.username
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
    # Сортируем балансы пользователей по убыванию
    leaderboard = sorted(user_balances.items(), key=lambda x: x[1], reverse=True)

    # Получаем username из сообщения пользователя
    username = message.from_user.username
    if not username:
        bot.send_message(message.chat.id, "У вас нет username, поэтому вы не можете участвовать в рейтинге.")
        return

    # Получаем баланс пользователя, если он есть, иначе 0
    user_balance = user_balances.get(username, 0)

    # Находим место пользователя в топе
    user_place = next((idx + 1 for idx, (name, _) in enumerate(leaderboard) if name == username), None)

    # Формируем строку с местом пользователя и его балансом
    if user_place:
        user_place_str = f"Ваше место в топе: {user_place}\nВаш баланс: {user_balance} шмеклей."
    else:
        # Если пользователя нет в таблице, добавляем его
        leaderboard.append((username, user_balance))
        leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)
        user_place = next((idx + 1 for idx, (name, _) in enumerate(leaderboard) if name == username), None)
        user_place_str = f"Ваше место в топе: {user_place}\n"

    # Отправляем пользователю его место в топе
    bot.send_message(message.chat.id, user_place_str)

    # Формируем и отправляем топ-10 лидеров
    leaders_str = "Топ 10 игроков:\n"
    for idx, (name, balance) in enumerate(leaderboard[:10], start=1):
        leaders_str += f"{idx}. @{name}: {balance} шмеклей.\n"

    bot.send_message(message.chat.id, leaders_str)

    # def update_crypto_values(username,user_balances, cryptocurrencies):
    balance = user_balances.get(username)
    crypto = cryptocurrencies.get(username)

    if crypto:
        # Рассчитываем изменение стоимости криптовалюты
        change_in_value = balance * crypto['total_value'] * 0.01

        # Обновляем общую стоимость криптовалюты
        crypto['total_value'] += change_in_value

        # Обновляем единичную стоимость криптовалюты
        if crypto['amount'] > 0:
            crypto['value'] = crypto['total_value'] / crypto['amount']

        # Сохраняем обновленные данные
        save_cryptocurrencies(cryptocurrencies)


# Используйте эту функцию в нужном месте вашего кода, например, после изменения баланса пользователя
# update_crypto_values(username, user_balances, cryptocurrencies)

@bot.message_handler(func=lambda message: message.text == 'Crypto')
def create_crypto(message):
    bot.send_message(message.chat.id, "Выбирай что нужно", reply_markup=markup_crypto)


@bot.message_handler(func=lambda message: message.text == 'Create Crypto')
def create_cryptocurrency(message):
    bot.reply_to(message, "Введите название вашей криптовалюты:")
    bot.register_next_step_handler(message, get_currency_name)


def get_currency_name(message):
    user_id = message.from_user.username
    currency_name = message.text
    if currency_name in cryptocurrencies:
        bot.send_message(message.chat.id, "Такая криптовалюта уже существует. Введите другое название:")
        bot.register_next_step_handler(message, get_currency_name)
    else:
        cryptocurrencies[user_id] = {'name': currency_name}
        bot.reply_to(message, f"Название криптовалюты: {currency_name}. Введите общую стоимость криптовалюты:")
        bot.register_next_step_handler(message, get_currency_value)


def get_currency_value(message):
    user_id = message.from_user.username
    balance = user_balances[user_id]
    currency_total_value = float(message.text)
    if currency_total_value <= balance:
        user_balances[user_id] -= currency_total_value
        cryptocurrencies[user_id]['total_value'] = currency_total_value
        bot.reply_to(message, f"Стоимость всей криптовалюты: {currency_total_value}. Введите количество криптовалюты:")
        bot.register_next_step_handler(message, get_currency_amount)
    else:
        bot.send_message(message.chat.id, "Недостаточно средств.Возвращаю назад")
        bot.send_message(message.chat.id, f"Введите общую стоимость криптовалюты:")
        bot.register_next_step_handler(message, get_currency_value)


def get_currency_amount(message):
    user_id = message.from_user.username
    currency_amount = float(message.text)
    cryptocurrencies[user_id]['amount'] = currency_amount
    bot.reply_to(message, "Криптовалюта успешно создана!")
    save_cryptocurrencies(cryptocurrencies)
    # Вывод информации о созданной криптовалюте
    user_currency = cryptocurrencies[user_id]
    currency_name = user_currency['name']
    currency_total_value = user_currency['total_value']
    currency_amount = user_currency['amount']
    currency_value = currency_total_value / currency_amount
    user_currency['value'] = currency_value
    bot.send_message(message.chat.id, f"Созданная криптовалюта: {currency_name}\n"
                                      f"Количество: {currency_amount}\n"
                                      f"Стоимость одной криптовалюты: {currency_value}\n"
                                      f"Общая стоимость: {currency_total_value}")
    if user_id not in crypto_data:
        crypto_data[user_id] = f"Название: {currency_name}, Общая стоимость: {currency_total_value}, Количество: {currency_amount}, За штуку: {currency_value}\n"
    else:
        crypto_data[user_id] += f"Название: {currency_name}, Общая стоимость: {currency_total_value}, Количество: {currency_amount}, За штуку: {currency_value}\n"

    save_crypto_data()


# Функция для покупки криптовалюты
@bot.message_handler(func=lambda message: message.text == 'Стать трейдером')
def buy_crypto(message):
    bot.send_message(message.chat.id, "Напишите название нужной вам криптовалюты(В точности до знака!)", reply_markup=markup_crypto)
    bot.register_next_step_handler(message, buy_cryptocurrency)


def buy_cryptocurrency(message):
    buyer_id = message.from_user.username
    seller_id = message.text

    # Проверка наличия криптовалюты у продавца
    if seller_id not in cryptocurrencies:
        bot.reply_to(message, "Продавец не имеет криптовалюты.")
        return

    # Получение информации о криптовалюте продавца
    currency_info = cryptocurrencies[seller_id]
    currency_value = currency_info['value']
    currency_amount = currency_info['amount']

    # Проверка наличия достаточного количества криптовалюты у продавца
    if currency_amount <= 0:
        bot.reply_to(message, "Криптовалюта у продавца недоступна для покупки.")
        return

    # Вычисление стоимости покупки
    balance = user_balances[buyer_id]
    desired_amount = 1  # Можно изменить на желаемое количество криптовалюты
    cost = currency_value * desired_amount

    # Проверка наличия достаточного баланса у покупателя
    if balance < cost:
        bot.reply_to(message, "У вас недостаточно средств для покупки.")
        return

    # Выполнение покупки
    user_balances[buyer_id] -= cost
    user_balances[seller_id] += cost  # Продавцу зачисляется сумма
    currency_info['amount'] -= desired_amount
    save_cryptocurrencies(cryptocurrencies)

    bot.reply_to(message, f"Вы успешно купили {desired_amount} криптовалюты у пользователя с user_id {seller_id} за {cost}.")


# Функция для отображения списка самых дорогих криптовалют
@bot.message_handler(func=lambda message: message.text == 'Топ крипт')
def show_top10(message):
    if not cryptocurrencies:
        bot.reply_to(message, "Еще нет созданных криптовалют. Возвращаю в меню", reply_markup=markup_menu)
        return

    top10 = sorted(cryptocurrencies.items(), key=lambda x: x[1]['total_value'], reverse=True)[:10]

    top10_message = "Топ 10 криптовалют по общей стоимости:\n"
    for idx, (currency_id, currency_data) in enumerate(top10, 1):
        currency_value = currency_data.get('total_value', 'Нет данных')  # Получение значения, если ключ существует, иначе строка 'Нет данных'
        currency_name = currency_data['name']
        username = currency_data.get('username', 'Нет данных')
        top10_message += f"{idx}. Автор: {username}, Название криптовалюты: {currency_name}, Общая стоимость: {currency_value}\n"

    bot.reply_to(message, top10_message, reply_markup=markup_menu)


@bot.message_handler(func=lambda message: message.text == 'Моя крипта')
def my_crypto(message):
    user_id = message.from_user.username
    if user_id in crypto_data:
        bot.send_message(message.chat.id, f"Мои криптовалюты:\n"
                                          f" {crypto_data[user_id]}")
    else:
        bot.send_message(message.chat.id, "У вас ещё нет криптовалют. Возвращаю в меню", reply_markup=markup_menu)


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
    user_id = message.from_user.username
    bot.send_message(message.chat.id, f"Твой ID: {user_id}", reply_markup=markup_info)


# Функция для перевода валюты
@bot.message_handler(func=lambda message: message.text == 'Напивкокенту!')
def send_money(message):
    bot.send_message(message.chat.id, "для начала выбери кентa, попроси его ID и подумай над суммой перевода.\n"
                                      "Когда решишься отправляй сообщение в формате(если выбираешь анон то сообщение старайся писать без пробелов): /перевод получатель сумма [анон]/[] сообщение\n"
                                      "Например: /перевод @alice 100 Привет, вот твои деньги - перевести 100 рублей пользователю с юзернеймом @alice с сообщением 'Привет, вот твои деньги'.\n"
                                      "/перевод @bob 50 анон За услуги - анонимный перевод 50 рублей пользователю с юзернеймом @bob с сообщением 'За услуги'.", reply_markup=markup_info)

    bot.register_next_step_handler(message, transfer_money)


def transfer_money(message):
    try:
        parts = message.text.split(maxsplit=4)
        if len(parts) < 4:
            bot.send_message(message.chat.id, "Некорректный формат. Используйте: /перевод @получатель сумма [анон] сообщение")
            return

        receiver_username = parts[1]
        amount = int(parts[2])
        sender_id = message.from_user.username
        is_anonymous = False
        message_text = ' '.join(parts[4:])

        if parts[3].lower() == "анон":
            is_anonymous = True

        if amount <= 0:
            bot.send_message(message.chat.id, "Сумма должна быть положительным числом.")
            bot.send_message(message.chat.id, "Попробуйте ещё раз.")
            bot.register_next_step_handler(message, transfer_money)
            return

        sender_balance = user_balances.get(sender_id)
        if sender_balance is None:
            bot.send_message(message.chat.id, "У вас нет средств для перевода.")
            bot.send_message(message.chat.id, "Попробуйте ещё раз.")
            bot.register_next_step_handler(message, transfer_money)
            return

        if sender_balance < amount:
            bot.send_message(message.chat.id, "У вас недостаточно средств для перевода этой суммы.")
            bot.send_message(message.chat.id, "Попробуйте ещё раз.")
            bot.register_next_step_handler(message, transfer_money)
            return

        if receiver_username not in user_balances:
            bot.send_message(message.chat.id, "Пользователь не найден.")
            bot.send_message(message.chat.id, "Попробуйте ещё раз.")
            bot.register_next_step_handler(message, transfer_money)
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
        bot.send_message(message.chat.id, "Некорректный формат. Используйте: /перевод ID сумма [анон/] сообщение")


@bot.message_handler(func=lambda message: message.text == 'Начнем возню')
def start_game(message):
    user_id = message.from_user.username
    if user_id not in user_balances:
        user_balances[user_id] = 1000
    balance = user_balances[user_id]
    bot.send_message(message.chat.id, f"Напомню, что твой баланс равен: {balance}рупий.\n"
                                      f"Теперь выбери игру.", reply_markup=markup_choise1)


@bot.message_handler(func=lambda message: message.text == 'Камень,Ножницы,Бумага')
def game_kamen1(message):
    user_id = message.from_user.username
    if user_id in in_game and in_game[user_id] == True:  # Проверяем, идет ли уже игра
        bot.send_message(message.chat.id, "Игра уже начата. Завершите текущую игру или выберите 'Еще раз'.")
        return

    in_game[user_id] = True
    bot.send_message(message.chat.id, 'Делай свой выбор,боров', reply_markup=markup_game1)
    bot.register_next_step_handler(message, game_kamen)


def game_kamen(message):
    user_id = message.from_user.username
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
    user_id = message.from_user.username
    if user_id in in_game and in_game[user_id] == True:  # Проверяем, идет ли уже игра
        bot.send_message(message.chat.id, "Игра уже начата. Завершите текущую игру или выберите 'Еще раз'.")
        return

    in_game[user_id] = True
    bot.send_message(message.chat.id, 'Ну что, боров, крути барабан', reply_markup=markup_game2)


@bot.message_handler(func=lambda message: message.text == 'Крутить барабан')
def russian_roulette(message):
    user_id = message.from_user.username
    balance = user_balances[user_id]
    if balance <= 0:
        bot.send_message(message.chat.id, "У вас недостаточно мани для игры.")
        return

    if random.randint(1, 6) == 1:
        with open(grystni_grigos, 'rb') as file:
            bot.send_photo(message.chat.id, file)
        user_balances[user_id] = 0  # Обнуляем баланс при проигрыше
        bot.send_message(message.chat.id, "Лудоман иди работай!")

    else:
        with open(happy_grigos, 'rb') as file:
            bot.send_photo(message.chat.id, file)
        user_balances[user_id] *= 2  # Увеличиваем баланс вдвое при выигрыше
        bot.send_message(message.chat.id, "Поздравляю! Вы победили и удвоили свой кэш.")
    bot.send_message(message.chat.id, f"Ваш текущий баланс: {user_balances[user_id]} евро", reply_markup=markup_game2)


@bot.message_handler(func=lambda message: message.text == 'Слоты')
def slots_game(message):
    user_id = message.from_user.username
    if user_id in in_game and in_game[user_id] == True:  # Проверяем, идет ли уже игра
        bot.send_message(message.chat.id, "Игра уже начата. Завершите текущую игру или выберите 'Еще раз'.")
        return

    in_game[user_id] = True
    bot.send_message(message.chat.id, 'Ну что, боров, ДЕЛАЙ СТАВКУ ЦИФРАМИ!!! (если хочешь сыграть еще раз просто напиши еще раз ставку)\n'
                                      'Чтобы выйти нажми вернуться в меню 2 раза', reply_markup=markup_info)

    bot.register_next_step_handler(message, play_slots)


def play_slots(message):
    user_id = message.from_user.username
    if user_id not in user_balances:  # Проверяем, идет ли уже игра
        bot.send_message(message.chat.id, "Вас нету в базе данных, попробуйте снова.")
        bot.register_next_step_handler(message, start)
        return
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

    symbols = ['💎', '🍀', '🔔', '🍊', '🍇', '🌟', '777', '🍒']  # Символы для слотов
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

    user_balances[user_id] = balance  # Обновляем баланс пользователя в словаре

    return reels, payout, balance


@bot.message_handler(func=lambda message: message.text == 'Еще раз')
def restart_game(message):
    user_id = message.from_user.username
    in_game[user_id] = False
    bot.send_message(message.chat.id, "Давай сыграем еще раз!", reply_markup=markup_game1)
    game_kamen1(message)  # Вызов функции game_kamen для начала новой игры


@bot.message_handler(func=lambda message: True)
def unknown(message):
    bot.send_message(message.chat.id, 'Извините, я вас не понимаю. Выберите то что вам нужно.', reply_markup=markup_menu)
    bot.register_next_step_handler(message, back_to_menu)


bot.polling()
