from telebot import types

import games.engine

chess_engine = games.engine.Engine

chess_symbols = {'bP': '♟', 'bR': '♜', 'bN': '♞', 'bB': '♝', 'bQ': '♛', 'bK': '♚',
                 'wP': '♙', 'wR': '♖', 'wN': '♘', 'wB': '♗', 'wQ': '♕', 'wK': '♔', '--': ' '}
""" Словарь символов для шахматных фигур. """

choice_symbols = ['!', '✔']
""" Список символов выбора. """

# Создание клавиш
button_give_up = types.InlineKeyboardButton(text='Сдаться', callback_data='give_up')
button_cancel = types.InlineKeyboardButton(text='Выбрать другую фигуру', callback_data='cancel')
button_stop = types.InlineKeyboardButton(text='Отменить поиск', callback_data='stop')

# Клавиатуры
def generate_main_keyboard(board, color):
    """
    Генерация основной игровой клавиатуры.

    :param board: Матрица доски
    :type board: list[list[str]]
    :param color: Цвет игрока
    :type color: str
    :return: Клавиатура
    """

    keyboard = types.InlineKeyboardMarkup(row_width=8)
    buttons = []

    if color == 'w':
        rng = 0, 8
    else:
        rng = 7, -1, -1

    for y in range(*rng):
        for x in range(*rng):
            chess_piece = board[y][x]
            chess_symbol = chess_symbols[chess_piece]
            callback_data = str(x) + ' ' + str(y)
            button = types.InlineKeyboardButton(text=chess_symbol, callback_data=callback_data)
            buttons.append(button)

    keyboard.add(*buttons)
    keyboard.add(button_give_up)
    return keyboard

def generate_choice_keyboard(board, xp, yp, color):
    """
    Генерация игровой клавиатуры с выбором хода.

    :param board: Матрица доски
    :type board: list[list[str]]
    :param xp: X фигуры
    :type xp: str
    :param yp: Y фигуры
    :type yp: str
    :param color: Цвет игрока
    :type color: str
    :return: При правильно выбранной фигуре - клавиатура, иначе строка для обработки ошибки
    """

    xp = int(xp)
    yp = int(yp)
    if board[yp][xp][0] == color:
        move_set = chess_engine.define_piece(xp, yp, color, board)
        keyboard = types.InlineKeyboardMarkup(row_width=8)
        buttons = []

        if color == 'w':
            rng = 0, 8
        else:
            rng = 7, -1, -1

        for y in range(*rng):
            for x in range(*rng):
                chess_piece = board[y][x]
                chess_symbol = chess_symbols[chess_piece]
                callback_data = str(x) + ' ' + str(y)
                if x == xp and y == yp:
                    chess_symbol = chess_symbol + choice_symbols[0]
                    callback_data = callback_data + ' !'
                elif (x, y) in move_set:
                    chess_symbol = chess_symbol + choice_symbols[1]
                    callback_data = callback_data + ' ✔'
                else:
                    callback_data = callback_data + ' ❌'
                button = types.InlineKeyboardButton(text=chess_symbol, callback_data=callback_data)
                buttons.append(button)

        keyboard.add(*buttons)
        keyboard.add(button_give_up, button_cancel)
        return keyboard
    elif board[yp][xp] == '--':
        return 'blank'
    else:
        return 'wrong'

def generate_pawn_keyboard(x, y, color):
    """
    Генерация клавиатуры для выбора превращения пешки.

    :param x: X фигуры
    :type x: str
    :param y: Y фигуры
    :type y: str
    :param color: Цвет игрока
    :type color: str
    :return: Клавиатура
    """

    keyboard = types.InlineKeyboardMarkup(row_width=4)
    buttons = []
    for choice in chess_engine.pawn_choice:
        chess_symbol = chess_symbols[color + choice]
        callback_data = x + ' ' + y + ' ' + choice + 'P'
        button = types.InlineKeyboardButton(text=chess_symbol, callback_data=callback_data)
        buttons.append(button)
    keyboard.add(*buttons)

    return keyboard

def stop_search_keyboard():
    """
    Создание клавиатуры отмены поиска.

    :return: Клавиатура
    """

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(button_stop)

    return keyboard
