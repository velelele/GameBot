from datetime import datetime, timedelta
from telebot import types
import json
import re
import glob
import os
from games.Battle import Battle
from config import config_see_battle
from get_rating import get_opp
from games import engine
from database.ban_db import Ban_DB
from handlers.play import victory_handler
from keyboard.print_keyboard import *
from games.Battle import All_Battle
from database import activity_db
chess_engine = engine.Engine


def run(bot):
    @bot.message_handler(func=lambda message: message.text == "Играть в морской бой")
    def play_see_battle_online(message):
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Приятной игры", reply_markup=keyboard)

        """
        Реакция бота на команду "/play_online".
        Помещение пользователя в очередь поиска соперника.
        При удачном поиске создание и вывод необходимой информации об игре.

        :param message: Информация о сообщении пользователя
        """

        ban_db = Ban_DB()

        with open('seebattle.json', 'r') as json_file:
            data = json.load(json_file)

        # Нельзя начать новую партию, если пользователь уже играет
        if message.chat.id in data['play']:
            bot.reply_to(message, 'Завершите партию для поиска нового соперника')

        # Если пользователь уже в очереди
        elif message.chat.id in data['search']:
            bot.reply_to(message, 'Вы уже в ожидание соперника')

        # Нельзя начать новую партию, если пользователь уже играет
        elif glob.glob('game' + str(message.chat.id) + str(message.chat.id) + '.json'):
            bot.reply_to(message, 'Завершите оффлайн-партию для начала онлайн-партии')

        elif ban_db.check_ban(message.chat.id):
            bot.send_message(message.chat.id, "Вы забанены и не можете играть, пока не получите разбан!")


        # Если в очереди уже кто-то есть - начинается игра
        elif data['search'] and get_opp(message.chat.id, data['game_name'][0]) != None:
            player = message.chat.id
            partner = get_opp(player, data['game_name'][0])

            date_now = datetime.now()
            game = activity_db.Matches(date=date_now, id_user1=player, id_user2=partner, name=data['game_name'][0])
            activity_db.add_game(game)

            battle_user = Battle(player, partner)
            battle_partner = Battle(partner, player)
            All_Battle[player] = battle_user
            All_Battle[partner] = battle_partner

            data['search'].remove(partner)
            data['play'].append(partner)
            data['play'].append(player)
            with open('seebattle.json.', 'w') as write_file:
                json.dump(data, write_file)

            w_name = bot.get_chat(partner).first_name
            b_name = bot.get_chat(player).first_name
            caption = w_name + ' VS ' + b_name + '\nХод ' + w_name

            battle_partner.add_ships_to_battlefield()
            board_image = open('images/game' + str(partner) + str(player) + data['game_name'][0] + '.png', 'rb')
            msg_w = bot.send_photo(partner, board_image, caption=caption,
                                   reply_markup=config_see_battle.generate_field_keyboard(battle_user.shots_fired))

            battle_user.add_ships_to_battlefield()
            board_image = open('images/game' + str(player) + str(partner) + data['game_name'][0] + '.png', 'rb')
            msg_b = bot.send_photo(player, board_image, caption=caption)

            game_data = {
                'chat_w': msg_w.chat.id,
                'chat_b': msg_b.chat.id,
                'turn': 'w',
            }
            with open('game' + str(game_data['chat_w']) + str(game_data['chat_b']) + data['game_name'][0] + '.json', 'w') as write_file:
                json.dump(game_data, write_file)

        # Если в очереди никого нет - в нее добавляется пользователь
        else:
            data['search'].append(message.chat.id)
            with open('seebattle.json.', 'w') as write_file:
                json.dump(data, write_file)

            markup = get_keyboard_stop()
            bot.send_message(message.chat.id, 'Ожидаем соперника...', reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text == "Сдаться")
    def give_up_handler(message):
        new_caption = ''
        old_caption = ''
        with open('seebattle.json', 'r') as json_file:
            data = json.load(json_file)
        file = glob.glob('game*' + str(message.chat.id) + '*' + data['game_name'][0] + '.json')
        if file:
            file = file[0]
            with open(file, 'r') as json_file:
                new_data = json.load(json_file)

            player_w = bot.get_chat(new_data['chat_w']).first_name
            player_b = bot.get_chat(new_data['chat_b']).first_name

            if new_data['chat_w'] == message.chat.id:
                victory_handler(new_data['chat_b'], new_data['chat_w'])
                new_caption = '\nВыиграл ' + player_b
            else:
                victory_handler(new_data['chat_w'], new_data['chat_b'])
                new_caption = '\nВыиграл ' + player_w

            bot.send_message(new_data['chat_b'], new_caption)
            bot.send_message(new_data['chat_w'], new_caption)

            with open('seebattle.json', 'r') as json_file:
                online_data = json.load(json_file)
            online_data['play'].remove(new_data['chat_w'])
            online_data['play'].remove(new_data['chat_b'])
            with open('seebattle.json.', 'w') as write_file:
                json.dump(online_data, write_file)

            os.remove('images/game' + str(new_data['chat_w']) + str(new_data['chat_b']) + data['game_name'][0] + '.png')
            os.remove('game' + str(new_data['chat_w']) + str(new_data['chat_b']) + data['game_name'][0] + '.json')
            keyboard = get_main_keyboard()
            bot.send_message(new_data['chat_w'], "Отличная игра!", reply_markup=keyboard)
            bot.send_message(new_data['chat_b'], "Отличная игра!", reply_markup=keyboard)

    @bot.message_handler(func=lambda message: message.text == "Остановить поиск")
    def stop(message):
        with open('seebattle.json', 'r') as json_file:
            data = json.load(json_file)
        data['search'].remove(message.chat.id)
        with open('seebattle.json.', 'w') as write_file:
            json.dump(data, write_file)
        keyboard = get_main_keyboard()
        bot.send_message(message.chat.id, 'Поиск соперника остановлен', reply_markup=keyboard)


    @bot.message_handler(func=lambda message: True)
    def arrangement_ships(message):
        if(check_variable_format(message.text)):
            with open('seebattle.json', 'r') as json_file:
                data = json.load(json_file)
            file = glob.glob('game*' + str(message.chat.id) + '*' + data['game_name'][0] + '.json')
            if file:
                file = file[0]
                with open(file, 'r') as json_file:
                    new_data = json.load(json_file)
                if new_data['chat_w'] == message.chat.id:
                    player = new_data['chat_w']
                    partner = new_data['chat_b']
                else:
                    player = new_data['chat_b']
                    partner = new_data['chat_w']
                field_opp = All_Battle.get(player).shots_fired
                x, y = ord(message.text[0].lower()) - ord('a'), int(message.text[1:]) - 1
                if field_opp[y][x] != None:
                    bot.send_message(player, "Вы уже стреляли сюда!")
                else:
                    shot = All_Battle.get(partner).receive_enemy_fire(message.text)
                    if shot:
                        battle_partner = All_Battle[partner]
                        battle_partner.add_ships_to_battlefield()

                        board_image_patrner = open('images/game' + str(partner) + str(player) + data['game_name'][0] + '.png', 'rb')
                        markup_user = config_see_battle.generate_field_keyboard(battle_partner.enemy_shots)
                        if battle_partner.hurt_or_kill(message.text) == "kill":
                            bot.send_message(player, "Вы потопили корабль! Стреляйте еще раз.", reply_markup=markup_user)
                            bot.send_photo(partner, board_image_patrner, "Ваш корабль потопили! Противник стреляет еще раз.")
                        else:
                            bot.send_message(player, "Вы ранили вражеский корабль! Стреляйте еще раз.", reply_markup= markup_user)
                            bot.send_photo(partner, board_image_patrner, "Ваш корабль ранили! Противник стреляет еще раз.")
                    else:
                        switch_turn(data, new_data, message, shot)


    def switch_turn(data, new_data, message, shot):
        """
        Передача хода другому игроку

        :param data: информация о партии
        :type data: dict
        :param new_caption: новое отображаемое сообщение
        :type new_caption: str
        :param call: Информация о действии пользователя
        :return:
        """

        cancel = False

        # В зависимости от цвета выбирается набор данных
        if new_data['turn'] == 'w':
            color_char = 'b'
            player_now = new_data['chat_w']
            player_next = new_data['chat_b']
        else:
            color_char = 'w'
            player_next = new_data['chat_w']
            player_now = new_data['chat_b']

        if not All_Battle[player_next].check_ships_alive():
            cancel = True
            end_game(message)

        # Если все проверки пройдены происходит смена хода
        if not cancel:
            """if chess_engine.check_pawn_upgrade(data['move_x'], data['move_y'], data['board']):
                new_caption += '\nВыберите фигуру'
                markup = config_chess.generate_pawn_keyboard(call.data[0], call.data[-3], data['turn'])
                bot.edit_message_caption(caption=new_caption, chat_id=data['chat_' + data['turn']],
                                         message_id=data['msg_' + data['turn']], reply_markup=markup)
            else:
                chess_engine.draw_board(new_board, data['chat_w'], data['chat_b'], data['turn'])
                board_image = open('images/game' + str(data['chat_w']) + str(data['chat_b']) + '.png', 'rb')
                if len(new_caption.split('\n')) == 3 and is_check_next:
                    new_caption = new_caption.split('\n')[0] + '\nХод ' + color_next + '\n' + new_caption.split('\n')[2]
                else:
                    new_caption = new_caption.split('\n')[0] + '\nХод ' + color_next

                bot.edit_message_media(media=types.InputMediaPhoto(board_image), chat_id=player_now,
                                       message_id=msg_now)
                bot.edit_message_caption(caption=new_caption, chat_id=player_now, message_id=msg_now)
"""
            game_data = {
                'chat_w': new_data['chat_w'],
                'chat_b': new_data['chat_b'],
                'turn': color_char
            }
            with open('game' + str(new_data['chat_w']) + str(new_data['chat_b']) + data['game_name'][0] + '.json', 'w') as write_file:
                json.dump(game_data, write_file)

            battle_user = All_Battle[player_now]
            battle_partner = All_Battle[player_next]

            #chess_engine.draw_board(game_data['board'], data['chat_w'], data['chat_b'], game_data['turn'])
            battle_user.add_ships_to_battlefield()
            battle_partner.add_ships_to_battlefield()
            board_image_user = open('images/game' + str(player_now) + str(player_next) + data['game_name'][0] + '.png', 'rb')
            board_image_patrner = open('images/game' + str(player_next) + str(player_now) + data['game_name'][0] + '.png', 'rb')
            markup_user = get_keyboard_get_up() #config_see_battle.generate_field_keyboard(battle_partner.enemy_shots)
            markup_partner = config_see_battle.generate_field_keyboard(battle_user.enemy_shots)
            bot.send_message(player_now, "Вы промазали! Ход противника", reply_markup=markup_user)
            bot.send_photo(player_next, board_image_patrner, "По вам не попали. Ваш ход.", reply_markup=markup_partner)

    def end_game(message):
        new_caption = ''
        old_caption = ''
        with open('seebattle.json', 'r') as json_file:
            data = json.load(json_file)
        file = glob.glob('game*' + str(message.chat.id) + '*' + data['game_name'][0] + '.json')
        if file:
            file = file[0]
            with open(file, 'r') as json_file:
                new_data = json.load(json_file)

            player_w = bot.get_chat(new_data['chat_w']).first_name
            player_b = bot.get_chat(new_data['chat_b']).first_name

            if data['turn'] == 'b':
                victory_handler(new_data['chat_b'], new_data['chat_w'])
                new_caption = '\nВыиграл ' + player_b
            else:
                victory_handler(new_data['chat_w'], new_data['chat_b'])
                new_caption = '\nВыиграл ' + player_w

            bot.send_message(new_data['chat_b'], new_caption)
            bot.send_message(new_data['chat_w'], new_caption)

            with open('seebattle.json', 'r') as json_file:
                online_data = json.load(json_file)
            online_data['play'].remove(new_data['chat_w'])
            online_data['play'].remove(new_data['chat_b'])
            with open('seebattle.json.', 'w') as write_file:
                json.dump(online_data, write_file)

            os.remove(
                'images/game' + str(new_data['chat_w']) + str(new_data['chat_b']) + data['game_name'][0] + '.png')
            os.remove('game' + str(new_data['chat_w']) + str(new_data['chat_b']) + data['game_name'][0] + '.json')
            keyboard = get_main_keyboard()
            bot.send_message(new_data['chat_w'], "Отличная игра!", reply_markup=keyboard)
            bot.send_message(new_data['chat_b'], "Отличная игра!", reply_markup=keyboard)


def check_variable_format(variable):
    pattern = r'^[A-Z]{1}[0-9]+'
    match = re.match(pattern, variable)
    if match:
        return True
    else:
        return False
