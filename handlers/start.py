from telebot import types
# from bot_functional.keyboards import keyboard_start
from keyboard.print_keyboard import get_post_keyboard


def run(bot):
    @bot.message_handler(commands=['start'])
    def start_command(message):
        keyboard_start = get_post_keyboard()
        bot.send_message(message.chat.id,"Выберите свою должность", reply_markup=keyboard_start)

