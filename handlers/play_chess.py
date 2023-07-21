from datetime import datetime
from telebot import types
import json
import glob
import os
from get_rating import get_opp
from games import engine
from handlers.play import victory_handler
from keyboard.print_keyboard import get_main_keyboard
from config import config_chess
from database.ban_db import Ban_DB
from database.activity_db import Activity_DB, Matches

chess_engine = engine.Engine
ban_db = Ban_DB()
activity_db = Activity_DB()

def run(bot):
    @bot.message_handler(func=lambda message: message.text == "Играть в шахматы")
    def play_chess_online(message):
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, "Приятной игры", reply_markup=keyboard)

        """
        Реакция бота на команду "/play_online".
        Помещение пользователя в очередь поиска соперника.
        При удачном поиске создание и вывод необходимой информации об игре.

        :param message: Информация о сообщении пользователя
        """

        with open('chess.json', 'r') as json_file:
            data = json.load(json_file)

        # Нельзя начать новую партию, если пользователь уже играет
        if message.chat.id in data['play']:
            keyboard = get_main_keyboard()
            bot.reply_to(message, 'Завершите партию для поиска нового соперника')

        # Если пользователь уже в очереди
        elif message.chat.id in data['search']:
            bot.reply_to(message, 'Вы уже в ожидание соперника')

        elif ban_db.check_ban(message.chat.id):
            bot.send_message(message.chat.id, "Вы забанены и не можете играть, пока не получите разбан!")

        # Если в очереди уже кто-то есть - начинается игра
        elif data['search'] and get_opp(message.chat.id, data['game_name'][0]) != None:
            player_b = message.chat.id
            player_w = get_opp(player_b, data['game_name'][0])
            date_now = datetime.now()
            match = Matches(match_date=date_now, player1_id=player_w, player2_id=player_b, name_game=data['game_name'][0])
            activity_db.add(match)
            data['search'].remove(player_w)
            data['play'].append(player_w)
            data['play'].append(player_b)
            with open('chess.json.', 'w') as write_file:
                json.dump(data, write_file)

            w_name = bot.get_chat(player_w).first_name
            b_name = bot.get_chat(player_b).first_name
            caption = w_name + '(Б) VS ' + b_name + '(Ч)\nХод белых'

            chess_engine.draw_board(chess_engine.start_board, player_w, player_b, 'w')
            board_image = open('images/game' + str(player_w) + str(player_b) + data['game_name'][0] + '.png', 'rb')

            msg_w = bot.send_photo(player_w, board_image, caption=caption,
                                   reply_markup=config_chess.generate_main_keyboard(chess_engine.start_board, 'w'))

            board_image = open('images/game' + str(player_w) + str(player_b) + data['game_name'][0] + '.png', 'rb')
            msg_b = bot.send_photo(player_b, board_image, caption=caption)

            game_data = {
                'msg_w': msg_w.message_id,
                'msg_b': msg_b.message_id,
                'chat_w': msg_w.chat.id,
                'chat_b': msg_b.chat.id,
                'turn': 'w',
                'board': chess_engine.start_board,
                'move_x': '',
                'move_y': '',
                'check_w': False,
                'check_b': False,
            }
            with open('game' + str(game_data['chat_w']) + str(game_data['chat_b']) + data['game_name'][0] + '.json', 'w') as write_file:
                json.dump(game_data, write_file)

        # Если в очереди никого нет - в нее добавляется пользователь
        else:
            data['search'].append(message.chat.id)
            with open('chess.json.', 'w') as write_file:
                json.dump(data, write_file)

            markup = config_chess.stop_search_keyboard()
            bot.send_message(message.chat.id, 'Ожидаем соперника...', reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        """
        Обработка действий, при нажатии игрока на кнопки.

        :param call: Информация о действии пользователя
        """

        if call.message:

            # Объявление, чтобы убрать warning'и
            new_caption = ''
            old_caption = ''

            # Если у пользователя есть партия
            file = glob.glob('game*' + str(call.message.chat.id) + '*.json')
            if file:
                file = file[0]
                with open(file, 'r') as json_file:
                    data = json.load(json_file)

                # Нарезка текста под картинкой доски, чтобы все правильно выводилось при разном тексте
                old_caption = call.message.caption
                if not data['check_w'] and not data['check_b']:
                    if len(call.message.caption.split('\n')) == 2:
                        new_caption = call.message.caption
                    else:
                        new_caption = call.message.caption.split('\n')[0] + '\n' + call.message.caption.split('\n')[1]
                else:
                    if len(call.message.caption.split('\n')) == 3:
                        new_caption = call.message.caption
                    else:
                        new_caption = call.message.caption.split('\n')[0] + '\n' + call.message.caption.split('\n')[1] + \
                                      '\n' + call.message.caption.split('\n')[2]

            # Кнопка 'Отменить поиск'
            if call.data == 'stop':
                with open('chess.json', 'r') as json_file:
                    data = json.load(json_file)
                data['search'].remove(call.message.chat.id)

                with open('chess.json.', 'w') as write_file:
                    json.dump(data, write_file)

                bot.edit_message_text('Поиск соперника остановлен', chat_id=call.message.chat.id,
                                      message_id=call.message.message_id)

            # Кнопка 'Сдаться'
            elif call.data == 'give_up':
                player_w = bot.get_chat(data['chat_w']).first_name
                player_b = bot.get_chat(data['chat_b']).first_name

                if data['turn'] == 'w':
                    victory_handler(bot.get_chat(data['chat_b']).id, bot.get_chat(data['chat_w']).id)
                    new_caption = new_caption.split('\n')[0] + '\nЧерные выиграли(' + player_b + ')'
                else:
                    victory_handler(bot.get_chat(data['chat_w']).id, bot.get_chat(data['chat_b']).id)
                    new_caption = new_caption.split('\n')[0] + '\nБелые выиграли(' + player_w + ')'

                if data['chat_w'] == data['chat_b']:
                    bot.edit_message_caption(caption=new_caption, chat_id=data['chat_w'], message_id=data['msg_w'])
                else:
                    bot.edit_message_caption(caption=new_caption, chat_id=data['chat_w'], message_id=data['msg_w'])
                    bot.edit_message_caption(caption=new_caption, chat_id=data['chat_b'], message_id=data['msg_b'])

                    with open('chess.json', 'r') as json_file:
                        online_data = json.load(json_file)
                    online_data['play'].remove(data['chat_w'])
                    online_data['play'].remove(data['chat_b'])
                    with open('chess.json.', 'w') as write_file:
                        json.dump(online_data, write_file)

                os.remove('images/game' + str(data['chat_w']) + str(data['chat_b']) + 'chess.png')
                os.remove('game' + str(data['chat_w']) + str(data['chat_b']) + 'chess.json')
                keyboard = get_main_keyboard()
                bot.send_message(data['chat_w'], "Отличная игра!", reply_markup=keyboard)
                bot.send_message(data['chat_b'], "Отличная игра!", reply_markup=keyboard)


            # Кнопка 'Выбрать другую фигуру'
            elif call.data == 'cancel':
                markup = config_chess.generate_main_keyboard(data['board'], data['turn'])
                bot.edit_message_reply_markup(reply_markup=markup, chat_id=data['chat_' + data['turn']],
                                              message_id=data['msg_' + data['turn']])

            # При нажатии на уже выбранную фигуру
            elif call.data[-1] == '!':
                new_caption += '\nФигура уже выбрана'
                markup = config_chess.generate_main_keyboard(data['board'], data['turn'])
                bot.edit_message_caption(caption=new_caption, chat_id=data['chat_' + data['turn']],
                                         message_id=data['msg_' + data['turn']], reply_markup=markup)

            # Сходить фигурой
            elif call.data[-1] == '✔':
                switch_turn(data, new_caption, call)

            # При превращении пешки
            elif call.data[-1] == 'P':
                data['board'][int(data['move_y'])][int(data['move_x'])] = data['turn'] + call.data[-2]
                call.data = call.data[:-1]
                switch_turn(data, new_caption, call)

            # При нажатии на невозможный ход
            elif call.data[-1] == '❌':
                new_caption += '\nСюда ходить нельзя'
                markup = config_chess.generate_main_keyboard(data['board'], data['turn'])
                bot.edit_message_caption(caption=new_caption, chat_id=data['chat_' + data['turn']],
                                         message_id=data['msg_' + data['turn']], reply_markup=markup)

            # Выбор фигуры
            else:
                markup = config_chess.generate_choice_keyboard(data['board'], call.data[0], call.data[-1], data['turn'])

                # Фигуры нет
                if markup == 'blank':
                    new_caption += '\nЗдесь нет фигуры'
                    if new_caption == old_caption:
                        new_caption += ' '
                    markup = config_chess.generate_main_keyboard(data['board'], data['turn'])
                    bot.edit_message_caption(caption=new_caption, chat_id=data['chat_' + data['turn']],
                                             message_id=data['msg_' + data['turn']], reply_markup=markup)

                # Фигура не своего цвета
                elif markup == 'wrong':
                    new_caption += '\nФигура не вашего цвета'
                    if new_caption == old_caption:
                        new_caption += ' '
                    markup = config_chess.generate_main_keyboard(data['board'], data['turn'])
                    bot.edit_message_caption(caption=new_caption, chat_id=data['chat_' + data['turn']],
                                             message_id=data['msg_' + data['turn']], reply_markup=markup)

                # Фигура своего цвета
                else:
                    game_data = {
                        'msg_w': data['msg_w'],
                        'msg_b': data['msg_b'],
                        'chat_w': data['chat_w'],
                        'chat_b': data['chat_b'],
                        'turn': data['turn'],
                        'board': data['board'],
                        'move_x': call.data[0],
                        'move_y': call.data[-1],
                        'check_w': data['check_w'],
                        'check_b': data['check_b'],
                    }
                    with open('game' + str(game_data['chat_w']) + str(game_data['chat_b']) + 'chess.json',
                              'w') as write_file:
                        json.dump(game_data, write_file)

                    bot.edit_message_caption(caption=new_caption, chat_id=data['chat_' + data['turn']],
                                             message_id=data['msg_' + data['turn']], reply_markup=markup)

    def switch_turn(data, new_caption, call):
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

        new_board = chess_engine.move_piece(data['move_x'], data['move_y'], call.data[0], call.data[-3],
                                            data['board'])
        is_check = chess_engine.check(new_board)

        # В зависимости от цвета выбирается набор данных
        if data['turn'] == 'w':
            color_next = 'черных'
            color_char = 'b'
            player_now = data['chat_w']
            player_next = data['chat_b']
            msg_now = data['msg_w']
            msg_next = data['msg_b']
            check_now = data['check_w']
            is_check_now = is_check['check_w']
            is_check_next = is_check['check_b']
        else:
            color_next = 'белых'
            color_char = 'w'
            player_next = data['chat_w']
            player_now = data['chat_b']
            msg_next = data['msg_w']
            msg_now = data['msg_b']
            check_now = data['check_b']
            is_check_next = is_check['check_w']
            is_check_now = is_check['check_b']

        # Если до начала хода союзный король был под шахом
        if check_now:
            # Если союзный король все еще под шахом
            if is_check_now:
                new_caption += '\nВаш король под шахом'
                markup = config_chess.generate_main_keyboard(data['board'], data['turn'])
                bot.edit_message_caption(caption=new_caption, chat_id=player_now, message_id=msg_now,
                                         reply_markup=markup)
                cancel = True
        else:
            # Если король соперника под шахом
            if is_check_next:
                new_caption = new_caption.split('\n')[0] + '\n' + new_caption.split('\n')[1] \
                              + '\nКороль ' + color_next + ' под угрозой'
            # Если союзный король поставлен под шах своим ходом
            elif is_check_now:
                new_caption += '\nВы не можете подставить своего короля'
                markup = config_chess.generate_main_keyboard(data['board'], data['turn'])
                bot.edit_message_caption(caption=new_caption, chat_id=player_now, message_id=msg_now,
                                         reply_markup=markup)
                cancel = True

        # Если все проверки пройдены происходит смена хода
        if not cancel:
            if chess_engine.check_pawn_upgrade(data['move_x'], data['move_y'], data['board']):
                new_caption += '\nВыберите фигуру'
                markup = config_chess.generate_pawn_keyboard(call.data[0], call.data[-3], data['turn'])
                bot.edit_message_caption(caption=new_caption, chat_id=data['chat_' + data['turn']],
                                         message_id=data['msg_' + data['turn']], reply_markup=markup)
            else:
                chess_engine.draw_board(new_board, data['chat_w'], data['chat_b'], data['turn'])
                board_image = open('images/game' + str(data['chat_w']) + str(data['chat_b']) + 'chess.png', 'rb')
                if len(new_caption.split('\n')) == 3 and is_check_next:
                    new_caption = new_caption.split('\n')[0] + '\nХод ' + color_next + '\n' + new_caption.split('\n')[2]
                else:
                    new_caption = new_caption.split('\n')[0] + '\nХод ' + color_next

                bot.edit_message_media(media=types.InputMediaPhoto(board_image), chat_id=player_now,
                                       message_id=msg_now)
                bot.edit_message_caption(caption=new_caption, chat_id=player_now, message_id=msg_now)

                game_data = {
                    'msg_w': data['msg_w'],
                    'msg_b': data['msg_b'],
                    'chat_w': data['chat_w'],
                    'chat_b': data['chat_b'],
                    'turn': color_char,
                    'board': new_board,
                    'move_x': '',
                    'move_y': '',
                    'check_w': is_check['check_w'],
                    'check_b': is_check['check_b'],
                }
                with open('game' + str(data['chat_w']) + str(data['chat_b']) + 'chess.json', 'w') as write_file:
                    json.dump(game_data, write_file)

                chess_engine.draw_board(game_data['board'], data['chat_w'], data['chat_b'], game_data['turn'])
                board_image = open('images/game' + str(data['chat_w']) + str(data['chat_b']) + 'chess.png', 'rb')
                markup = config_chess.generate_main_keyboard(game_data['board'], game_data['turn'])

                bot.edit_message_media(media=types.InputMediaPhoto(board_image), chat_id=player_next,
                                       message_id=msg_next)
                bot.edit_message_caption(caption=new_caption, chat_id=player_next, message_id=msg_next,
                                         reply_markup=markup)

