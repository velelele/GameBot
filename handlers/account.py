from telebot import types
from admin import *
from database.player_db import Player_DB
from keyboard.print_keyboard import *
from database.ban_db import Ban_DB

ban_db = Ban_DB()
player_db = Player_DB()

def run(bot):
    @bot.message_handler(func = lambda message : message.text in ["Посмотреть личный кабинет", "Вернуться в личный кабинет"])
    def definition_position(message):
        post = player_db.definition_post(message.from_user.id)
        keyboard = get_keyboard_account(post)
        bot.send_message(message.chat.id, "Выберите, что хотите сделать", reply_markup=keyboard)

    @bot.message_handler(func=lambda message: message.text == "Выйти в главное меню")
    def btn_back(message):
        main_keyboard = get_main_keyboard()
        bot.send_message(message.chat.id,"Выберите, что хотите сделать", reply_markup=main_keyboard)

    @bot.message_handler(func=lambda message: message.text == "Посмотреть информацию о себе")
    def print_personal_data(message):
        result = get_info_acc(message.from_user.id)
        keyboard_back = get_keyboard_account(player_db.definition_post(message.from_user.id))
        bot.send_message(message.chat.id,result, reply_markup=keyboard_back)

    @bot.message_handler(func=lambda message: message.text == "Посмотреть информацию о всех пользователях")
    def print_all_person(message):
        result = get_info_all()
        keyboard_back = get_keyboard_account(player_db.definition_post(message.from_user.id))
        bot.send_message(message.chat.id, result, reply_markup=keyboard_back)

    @bot.message_handler(func=lambda message: message.text == "Топ 10 игроков")
    def print_top(message):
        result = get_top()
        keyboard_back = get_keyboard_back()
        bot.send_message(message.chat.id, result, reply_markup=keyboard_back)

    @bot.message_handler(func=lambda message: message.text == "Посмотреть информацию о конкретном пользователе")
    def profile_definition(message):
        bot.register_next_step_handler(message, check_id)
        keyboard = get_keyboard_id(player_db.get_all())
        bot.send_message(message.chat.id, "Выберите id пользователя, о котором хотите посмотреть информацию", reply_markup=keyboard)


    #@bot.message_handler(func=lambda message: message.reply_to_message is not None and message.content_type == 'text')
    def check_id(message):
        id = get_id(message)
        info = get_info_acc(id)
        keyboard = get_keyboard_account(player_db.definition_post(message.from_user.id))
        bot.send_message(message.chat.id, info, reply_markup=keyboard)

    @bot.message_handler(func=lambda message: message.text == "Посмотреть информацию о новых пользователях пользователях")
    def check_new_acc(message):
        bot.register_next_step_handler(message, get_new_acc)
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите количество дней, за которое хотите получить"
                                          "количество новых пользователей(только число)", reply_markup= keyboard)

    def get_new_acc(message):
        day = message.text
        if day.isdigit():
            info = get_info_new_user(day)
            keyboard = get_keyboard_account(player_db.definition_post(message.from_user.id))
            bot.send_message(message.chat.id, info, reply_markup=keyboard)
        else:
            keyboard = get_keyboard_back()
            bot.send_message(message.chat.id, "Вы ввели некорректные данные", reply_markup=keyboard)

    @bot.message_handler(func=lambda message: message.text == "Посмотреть информацию об активности")
    def check_act(message):
        bot.register_next_step_handler(message, get_activity)
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите количество дней, за которое хотите получить"
                                          "информацию об активности пользователей(только число)", reply_markup=keyboard)

    def get_activity(message):
        day = message.text
        if day.isdigit():
            info = get_info_activity(day)
            keyboard = get_keyboard_account(player_db.definition_post(message.from_user.id))
            bot.send_message(message.chat.id, info, reply_markup=keyboard)
        else:
            keyboard = get_keyboard_back()
            bot.send_message(message.chat.id, "Вы ввели некорректные данные", reply_markup=keyboard)

    @bot.message_handler(func=lambda message: message.text == "Добавить пользователя в бан")
    def ban(message):
        bot.register_next_step_handler(message, add_ban)
        keyboard = get_keyboard_id(player_db.get_all())
        bot.send_message(message.chat.id, "Выберите id пользователя, которому хотите даль бан", reply_markup=keyboard)

    def add_ban(message):
        id = get_id(message)
        if ban_db.check_ban(id):
            result = "Пользователь уже забанен!"
        else:
            if upgrade_user_ban(id, True):
                info = get_info_acc(id)
                result = "Пользователь забанен!\n\n" + info
            else:
                result = "Пользователя с таким id не существует!"
        keyboard = get_keyboard_account(player_db.definition_post(message.from_user.id))
        bot.send_message(message.chat.id, result, reply_markup=keyboard)

    @bot.message_handler(func=lambda message: message.text == "Убрать пользователю бан")
    def not_ban(message):
        bot.register_next_step_handler(message, remove_ban)
        keyboard = get_keyboard_id(player_db.get_all())
        bot.send_message(message.chat.id, "Выберите id пользователя, у которого хотите убрать бан", reply_markup=keyboard)

    def remove_ban(message):
        id = get_id(message)
        if not ban_db.check_ban(id):
            result = "Пользователь не был забанен!"
        else:
            if upgrade_user_ban(id, False):
                info = get_info_acc(id)
                result = "Пользователь разбанен!\n\n" + info
            else:
                result = "Пользователя с таким id не существует!"
        keyboard = get_keyboard_account(player_db.definition_post(message.from_user.id))
        bot.send_message(message.chat.id, result, reply_markup=keyboard)

    @bot.message_handler(func=lambda message: message.text == "Изменить количество токенов пользователю")
    def token(message):
        bot.register_next_step_handler(message, choice_id_for_token)
        keyboard = get_keyboard_id(player_db.get_all())
        bot.send_message(message.chat.id, "Выберите id пользователя, у которого хотите изменить количество токенов",
                         reply_markup=keyboard)

    def choice_id_for_token(message):
        id = get_id(message)
        keyboard = types.ReplyKeyboardRemove()
        bot.register_next_step_handler(message, lambda next_message: upgrade_token(next_message, id))
        bot.send_message(message.chat.id, "Напишите количество токенов, которое будет у пользователя",
                         reply_markup=keyboard)

    def upgrade_token(next_message, id):
        token = next_message.text
        if token.isdigit():
            if upgrade_user_token(id, token):
                info = get_info_acc(id)
                result = "Количество токенов изменено!\n\n" + info
            else:
                result = "Пользователя с таким id не существует!"
            keyboard = get_keyboard_account(player_db.definition_post(next_message.from_user.id))
            bot.send_message(next_message.chat.id, result, reply_markup=keyboard)
        else:
            keyboard = get_keyboard_back()
            bot.send_message(next_message.chat.id, "Вы ввели некорректные данные", reply_markup=keyboard)


    def get_id(text):
        id = text.text.split(";")[1].strip()
        return id
