from database.player_db import Player_DB
import datetime
from telebot import types
from database.player_db import Player
from database.interfaceDB import DB_Interface
from keyboard.print_keyboard import get_main_keyboard, get_keyboard_false_admin_key

main_keyboard = get_main_keyboard()
player_db = Player_DB()

def run(bot):
    @bot.message_handler(func = lambda message : message.text in ["Администратор", "Попробовать снова"])
    def admin_registration(message):
        bot.register_next_step_handler(message, check_key)
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Введите ключ", reply_markup=keyboard)

    #@bot.message_handler(func = lambda message : message.text == "admin")
    def check_key(message):
        entered_key = message.text
        if entered_key == "admin":
            bot.register_next_step_handler(message, add_admin)
            bot.send_message(message.chat.id, "Придумайте пароль(Не более 10 символов, пожалуйста)")
        else:
            keyboard_false_admin_key = get_keyboard_false_admin_key()
            bot.send_message(message.chat.id, "Неправильный ключ! Вы хотите попробовать снова или зарегистрироваться как игрок?",reply_markup=keyboard_false_admin_key)
        #elif message.reply_to_message.text == "Введите в ответ на это сообщение id профиля":
            #await print_person(message)

    def add_admin(message):
        user = Player(name_player=bot.get_chat(message.chat.id).first_name, id=message.from_user.id,
                      registration_date=datetime.date.today(), position="Администратор", password=message.text)
        if player_db.add(user):
            bot.send_message(message.chat.id, f"Поздравляем, вы зарегистроровались, как {user.position}",
                             reply_markup=main_keyboard)
        else:
            bot.send_message(message.chat.id, f"Вы уже зарегистрированы!",
                             reply_markup=main_keyboard)

    @bot.message_handler(func = lambda message : message.text in ["Игрок", "Зарегистрироваться как игрок"])
    def player_registration(message):
        bot.register_next_step_handler(message, add_player)
        bot.send_message(message.chat.id, "Придумайте пароль(Не более 10 символов, пожалуйста)")

    def add_player(message):
        user = Player(name_player=bot.get_chat(message.chat.id).first_name, id=message.from_user.id,
                      registration_date=datetime.date.today(), position="Игрок", password=message.text)
        if player_db.add(user):
            bot.send_message(message.chat.id, f"Поздравляем, вы зарегистроровались, как {user.position}",
                             reply_markup=main_keyboard)
        else:
            bot.send_message(message.chat.id, f"Вы уже зарегистрированы!",
                             reply_markup=main_keyboard)

