import json
from database.player_db import  Player_DB
player_db = Player_DB()
def get_opp(tg_id, game):
    rating_user = player_db.get(tg_id).token
    if game == "chess":
        with open('chess.json', 'r') as json_file:
            data = json.load(json_file)
    elif game == "see_battle":
        with open('seebattle.json', 'r') as json_file:
            data = json.load(json_file)

    gamers = {}
    for id in data['search']:
        gamers[id] = player_db.get(id).token

    closest_key = None
    min_difference = float('inf')  # Начальное значение минимальной разницы, установленной на бесконечность
    for key, value in gamers.items():
        difference = abs(value - rating_user)  # Разница между текущим значением и целевым значением
        if difference < min_difference and difference < 50:
            min_difference = difference
            closest_key = key

    return closest_key