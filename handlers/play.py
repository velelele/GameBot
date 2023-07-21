from database.player_db import Player_DB
from database.win_loss_db import Result_Battle_DB
from database.rating_db import Rating_DB
from keyboard.print_keyboard import get_keyboard_game


def run(bot):
    @bot.message_handler(func=lambda message: message.text == "Играть")
    def play_chess_online(message):
        keyboard = get_keyboard_game()
        bot.send_message(message.chat.id, "Во что хотите поиграть?", reply_markup=keyboard)


def victory_handler(id_winner, id_loser):
    player_db = Player_DB()
    rating_db = Rating_DB()
    result_db = Result_Battle_DB()
    winner = player_db.get(id_winner)
    loser = player_db.get(id_loser)
    result_db.add_win(id_winner, winner.wins_cnt + 1)
    result_db.add_lose(id_loser, loser.losses_cnt + 1)
    if winner.token > loser.token:
        rating_db.set(id_winner, winner.token + 8)
        rating_db.set(id_loser, loser.token - 8)
    elif winner.token < loser.token:
        rating_db.set(id_winner, winner.token + 12)
        rating_db.set(id_loser, loser.token - 12)
    else:
        rating_db.set(id_winner, winner.token + 10)
        rating_db.set(id_loser, loser.token - 10)
