import telebot
import importlib
import os

from games import engine


token = ''
""" Токен бота. """

bot = telebot.TeleBot(token)
chess_engine = engine.Engine




# Команды бота
for x in os.listdir("./handlers/"):
    if x.endswith(".py"):
        module_name = "handlers." + x[:-3]
        try:
            cog = importlib.import_module(module_name)
            cog.run(bot)
        except ImportError as e:
            print(f"Error importing module {module_name}: {e}")


# Основная функция бота
bot.polling()
