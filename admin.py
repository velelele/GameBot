from database.player_db import Player_DB
import re
from database.activity_db import Activity_DB
from database.ban_db import Ban_DB
from database.rating_db import Rating_DB

rating_db = Rating_DB()
player_db = Player_DB()
ban_db = Ban_DB()
activity_db = Activity_DB()

"""
Посмотреть есть ли у пользователя бан
"""
def get_user_ban(tg_id):
    ban = ban_db.check_ban(tg_id)
    if ban:
        return "Активен"
    else:
        return "Не активен"

"""
Изменить пользователю состояние бана
"""
def upgrade_user_ban(tg_id, ban):
    if player_db.exists(tg_id):
        ban_db.set(tg_id, ban)
        return True
    else:
        return False


"""
Изменить пользователю количество токенов
"""
def upgrade_user_token(tg_id, token):
    if player_db.exists(tg_id):
        rating_db.set(tg_id, int(token))
        return True
    else:
        return False

"""
Посмотреть полную информацию об одном аккаунте
"""
def get_info_acc(tg_id):
    if player_db.exists(tg_id):
        user = player_db.get(tg_id)
        ban = get_user_ban(tg_id)
        data_string = f"Имя: {user.name}\n"\
                      f"Рейтинг: {user.token} 🏆 \n" \
                      f"Бан: {ban}\n" \
                      f"Количество побед: {user.wins_cnt}\n" \
                      f"Колчество проигрышей: {user.losses_cnt}\n" \
                      f"Дата регистрации: {user.date_registration}\n" \
                      f"Должность: {user.post}"
        return data_string

"""
Посмотреть список всех пользователей и краткую информацию о них
"""
def get_info_all():
    users = player_db.get_all()
    result = ""
    for user in users:
        ban = get_user_ban(user.tg_id)
        result += f"Имя: {user.name}; id: {user.tg_id}; Рейтинг: {user.token}; Бан: {ban}\n"
    return result

def get_id(message):
    pattern = r"\d+;\s[\w\s]+"
    if re.match(pattern, message):
        parts = message.split(";")
        id = parts[0]
        return id


"""
Посмотреть информацию об активности пользователей
"""
def get_purpose(message):
    pattern = r"\d+;\s[\w\s]+"
    if re.match(pattern, message):
        parts = message.split(";")
        text = parts[1].strip()
        return text


"""
Посмотреть информацию о том, сколько новых пользователей зарегистрировались
за последние несколько дней
"""
def get_info_new_user(cnt_day):
    users = player_db.check_new_user(int(cnt_day))
    i = 0
    result = f"Зарегистрировалось {len(users)} новых пользователей:\n"
    for user in users:
        i+=1
        result += f"{i+1}. Имя: {user.name}; id: {user.tg_id}; Рейтинг: {user.token}🏆\n"
    return result

"""
Посмотреть топ лучших игроков
"""
def get_top():
    users = player_db.get_all()

    length = len(users)
    if length >= 10:
        length = 10
    result = ""

    sorted_users = sorted(users, key=lambda u: u.token, reverse=True)

    for i in range(length):
        user = sorted_users[i]
        result += f"{i+1}. Имя: {user.name}; Рейтинг: {user.token}🏆\n"

    return result


"""
Посмотреть информацию об активности пользователей
"""
def get_info_activity(day):
    info = activity_db.check_activity(int(day))
    result = f"За последние несколько({day}) дней было сыграно {len(info)} игр"
    return result