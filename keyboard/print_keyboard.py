from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from games.games_list import games

def get_main_keyboard():
    main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btns = [KeyboardButton("Играть"), KeyboardButton("Посмотреть личный кабинет")]
    for btn in btns:
        main_keyboard.add(btn)
    return main_keyboard

def get_post_keyboard():
    post_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btns = [KeyboardButton("Игрок"), KeyboardButton("Администратор")]
    for btn in btns:
        post_keyboard.add(btn)
    return post_keyboard

def get_keyboard_false_admin_key():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btns = [KeyboardButton("Попробовать снова"),
            KeyboardButton("Зарегистрироваться как игрок")]
    for btn in btns:
        keyboard.add(btn)
    return keyboard

def get_keyboard_account(post):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btns = [KeyboardButton("Посмотреть информацию о себе"),
            KeyboardButton("Топ 10 игроков")]
    if post == "Администратор":
        btns.append("Посмотреть информацию о всех пользователях")
        btns.append("Посмотреть информацию о конкретном пользователе")
        btns.append("Посмотреть информацию о новых пользователях пользователях")
        btns.append("Посмотреть информацию об активности")
        btns.append("Добавить пользователя в бан")
        btns.append("Убрать пользователю бан")
        btns.append("Изменить количество токенов пользователю")
    btns.append("Выйти в главное меню")
    for btn in btns:
        keyboard.add(btn)
    return keyboard

def get_keyboard_game():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for game in games:
        btn = KeyboardButton("Играть в " + game)
        keyboard.add(btn)
    return keyboard

def get_keyboard_back():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    """KeyboardButton("Изменить кол-во токенов"),
                KeyboardButton("Внести в бан"), KeyboardButton("Достать из бана"),"""
    btns = [KeyboardButton("Выйти в главное меню"), KeyboardButton("Вернуться в личный кабинет")]
    for btn in btns:
        keyboard.add(btn)
    return keyboard

def get_keyboard_get_up():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("Сдаться")
    keyboard.add(btn)
    return keyboard

def get_keyboard_stop():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton("Остановить поиск")
    keyboard.add(btn)
    return keyboard

def get_keyboard_id(users):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for user in users:
        btn = KeyboardButton(f"{user.name}; {user.tg_id}")
        keyboard.add(btn)
    return keyboard



