from PIL import Image

class Engine:
    """ Класс с логикой игры и отрисовки шахматной доски. """

    images = {'bP': Image.open('./images/bP.png'), 'bR': Image.open('./images/bR.png'), 'bN': Image.open(
        './images/bN.png'),
              'bB': Image.open('./images/bB.png'), 'bQ': Image.open('./images/bQ.png'), 'bK': Image.open(
            './images/bK.png'),
              'wP': Image.open('./images/wP.png'), 'wR': Image.open('./images/wR.png'), 'wN': Image.open(
            './images/wN.png'),
              'wB': Image.open('./images/wB.png'), 'wQ': Image.open('./images/wQ.png'), 'wK': Image.open(
            './images/wK.png')}
    """ Словарь с изображениями фигур. """

    start_board = [
        ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
        ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['--', '--', '--', '--', '--', '--', '--', '--'],
        ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
        ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
    ]
    """ Матрица стартовой шахматной доски. """

    pawn_choice = ['R', 'N', 'B', 'Q']
    """ Список возможных превращений пешки, когда она доходит до конца доски. """

    @staticmethod
    def draw_board(board, player1_id, player2_id, color):
        """
        Создание png картинки шахматной доски.

        :param board: Матрица шахматной доски
        :type board: list[list[str]]
        :param player1_id: Id первого игрока
        :param player2_id: Id второго игрока
        :param color: Цвет игрока
        :type color: str
        """

        board_image = Image.new("RGB", (8, 8), (180, 180, 180))
        pixels = board_image.load()

        for y in range(8):
            for x in range(8):
                if (x + y) % 2 == 1:
                    pixels[y, x] = (255, 255, 255)
        board_image = board_image.resize((60 * 8, 60 * 8), Image.NEAREST)

        for y in range(8):
            for x in range(8):
                if color == 'w':
                    offset = (x * 60, y * 60)
                else:
                    offset = (420 - x * 60, 420 - y * 60)
                chess_piece = board[y][x]
                if chess_piece != '--':
                    board_image.paste(Engine.images.get(chess_piece), offset, mask=Engine.images.get(chess_piece))

        board_image.save('images/game' + str(player1_id) + str(player2_id) + 'chess.png', 'PNG')

    @staticmethod
    def check_range(x, y):
        """
        Проверка на существование клетки шахматной доски.

        :param x: X клетки
        :type x: int
        :param y: Y клетки
        :type y: int
        :return: Результат проверки
        """

        if x in range(8) and y in range(8):
            return True
        else:
            return False

    @staticmethod
    def move_piece(xp, yp, x, y, board):
        """
        Cдвиг выбранной фигуры. Возвращает новую матрицу доски.

        :param xp: X фигуры
        :type xp: str
        :param yp: Y фигуры
        :type yp: str
        :param x: X клетки
        :type x: str
        :param y: Y клетки
        :type y: str
        :param board: Матрица шахматной доски
        :return: Матрица шахматной доски со сдвинутой фигурой
        :rtype: list[list[str]]
        """

        xp = int(xp)
        yp = int(yp)
        x = int(x)
        y = int(y)
        board_copy = [x[:] for x in board]

        if board_copy[y][x] == '--':
            board_copy[yp][xp], board_copy[y][x] = board_copy[y][x], board_copy[yp][xp]
        else:
            board_copy[yp][xp], board_copy[y][x] = '--', board_copy[yp][xp]
        return board_copy

    @staticmethod
    def define_piece(x, y, color, board):
        """
        Определяет тип фигуры и вызывает для нее функцию определения возможных ходов.

        :param x: X фигуры
        :type x: int
        :param y: Y фигуры
        :type y: int
        :param color: Цвет игрока
        :type color: str
        :param board: Матрица доски
        :type board: list[list[str]]
        :return: Список возможных ходов
        :rtype: list[tuple]
        """

        chess_piece = board[y][x][1]
        if chess_piece == 'P':
            return Engine.pawn(x, y, color, board)
        if chess_piece == 'R':
            return Engine.rook(x, y, color, board)
        if chess_piece == 'N':
            return Engine.knight(x, y, color, board)
        if chess_piece == 'B':
            return Engine.bishop(x, y, color, board)
        if chess_piece == 'Q':
            return Engine.queen(x, y, color, board)
        if chess_piece == 'K':
            return Engine.king(x, y, color, board)

    # Функции определения возможных ходов
    @staticmethod
    def pawn(x, y, color, board):
        """
        Определяет возможные ходы для пешки.

        :param x: X фигуры
        :type x: int
        :param y: Y фигуры
        :type y: int
        :param color: Цвет игрока
        :type color: str
        :param board: Матрица доски
        :type board: list[list[str]]
        :return: Список возможных ходов
        :rtype: list[tuple]
        """

        move_set = []
        if (Engine.check_range(x, y + 1) and board[y + 1][x] == '--' and color == 'b') \
                or (Engine.check_range(x, y - 1) and board[y - 1][x] == '--' and color == 'w'):
            if color == 'b':
                move_set.append((x, y + 1))
            else:
                move_set.append((x, y - 1))

            if (y == 1 and color == 'b' and board[y + 2][x] == '--') \
                    or (y == 6 and color == 'w' and board[y - 2][x] == '--'):
                if color == 'b':
                    move_set.append((x, y + 2))
                else:
                    move_set.append((x, y - 2))
        if color == 'b':
            if Engine.check_range(x + 1, y + 1) and board[y + 1][x + 1][0] == 'w':
                move_set.append((x + 1, y + 1))
            if Engine.check_range(x - 1, y + 1) and board[y + 1][x - 1][0] == 'w':
                move_set.append((x - 1, y + 1))
        else:
            if Engine.check_range(x + 1, y - 1) and board[y - 1][x + 1][0] == 'b':
                move_set.append((x + 1, y - 1))
            if Engine.check_range(x - 1, y - 1) and board[y - 1][x - 1][0] == 'b':
                move_set.append((x - 1, y - 1))

        return move_set

    @staticmethod
    def rook(x, y, color, board):
        """
        Определяет возможные ходы для ладьи.

        :param x: X фигуры
        :type x: int
        :param y: Y фигуры
        :type y: int
        :param color: Цвет игрока
        :type color: str
        :param board: Матрица доски
        :type board: list[list[str]]
        :return: Список возможных ходов
        :rtype: list[tuple]
        """

        move_set = []
        flag = True
        for i in range(1, 8 - y):
            if Engine.check_range(x, y + i) and flag:
                if board[y + i][x] == '--':
                    move_set.append((x, y + i))
                else:
                    if board[y + i][x][0] == color:
                        flag = False
                    else:
                        move_set.append((x, y + i))
                        flag = False

        flag = True
        for i in range(1, y + 1):
            if Engine.check_range(x, y - i) and flag:
                if board[y - i][x] == '--':
                    move_set.append((x, y - i))
                else:
                    if board[y - i][x][0] == color:
                        flag = False
                    else:
                        move_set.append((x, y - i))
                        flag = False

        flag = True
        for i in range(1, 8 - x):
            if Engine.check_range(x + i, y) and flag:
                if board[y][x + i] == '--':
                    move_set.append((x + i, y))
                else:
                    if board[y][x + i][0] == color:
                        flag = False
                    else:
                        move_set.append((x + i, y))
                        flag = False

        flag = True
        for i in range(1, x + 1):
            if Engine.check_range(x - i, y) and flag:
                if board[y][x - i] == '--':
                    move_set.append((x - i, y))
                else:
                    if board[y][x - i][0] == color:
                        flag = False
                    else:
                        move_set.append((x - i, y))
                        flag = False

        return move_set

    @staticmethod
    def knight(x, y, color, board):
        """
        Определяет возможные ходы для коня.

        :param x: X фигуры
        :type x: int
        :param y: Y фигуры
        :type y: int
        :param color: Цвет игрока
        :type color: str
        :param board: Матрица доски
        :type board: list[list[str]]
        :return: Список возможных ходов
        :rtype: list[tuple]
        """

        moves = [(x + 2, y + 1), (x + 2, y - 1), (x - 2, y + 1), (x - 2, y - 1), (x + 1, y + 2), (x + 1, y - 2),
                 (x - 1, y + 2), (x - 1, y - 2)]
        move_set = []
        for move in moves:
            if Engine.check_range(move[0], move[1]):
                if board[move[1]][move[0]] == '--' or board[move[1]][move[0]][0] != color:
                    move_set.append(move)

        return move_set

    @staticmethod
    def bishop(x, y, color, board):
        """
        Определяет возможные ходы для слона.

        :param x: X фигуры
        :type x: int
        :param y: Y фигуры
        :type y: int
        :param color: Цвет игрока
        :type color: str
        :param board: Матрица доски
        :type board: list[list[str]]
        :return: Список возможных ходов
        :rtype: list[tuple]
        """

        move_set = []
        flag = True
        for i in range(1, 8 - y):
            if Engine.check_range(x + i, y + i) and flag:
                if board[y + i][x + i] == '--':
                    move_set.append((x + i, y + i))
                else:
                    if board[y + i][x + i][0] == color:
                        flag = False
                    else:
                        move_set.append((x + i, y + i))
                        flag = False

        flag = True
        for i in range(1, 8 - y):
            if Engine.check_range(x - i, y + i) and flag:
                if board[y + i][x - i] == '--':
                    move_set.append((x - i, y + i))
                else:
                    if board[y + i][x - i][0] == color:
                        flag = False
                    else:
                        move_set.append((x - i, y + i))
                        flag = False

        flag = True
        for i in range(1, y + 1):
            if Engine.check_range(x + i, y - i) and flag:
                if board[y - i][x + i] == '--':
                    move_set.append((x + i, y - i))
                else:
                    if board[y - i][x + i][0] == color:
                        flag = False
                    else:
                        move_set.append((x + i, y - i))
                        flag = False

        flag = True
        for i in range(1, y + 1):
            if Engine.check_range(x - i, y - i) and flag:
                if board[y - i][x - i] == '--':
                    move_set.append((x - i, y - i))
                else:
                    if board[y - i][x - i][0] == color:
                        flag = False
                    else:
                        move_set.append((x - i, y - i))
                        flag = False

        return move_set

    @staticmethod
    def queen(x, y, color, board):
        """
        Определяет возможные ходы для королевы.

        :param x: X фигуры
        :type x: int
        :param y: Y фигуры
        :type y: int
        :param color: Цвет игрока
        :type color: str
        :param board: Матрица доски
        :type board: list[list[str]]
        :return: Список возможных ходов
        :rtype: list[tuple]
        """

        move_set = Engine.rook(x, y, color, board)[:]
        move_set += Engine.bishop(x, y, color, board)[:]

        return move_set

    @staticmethod
    def king(x, y, color, board):
        """
        Определяет возможные ходы для короля.

        :param x: X фигуры
        :type x: int
        :param y: Y фигуры
        :type y: int
        :param color: Цвет игрока
        :type color: str
        :param board: Матрица доски
        :type board: list[list[str]]
        :return: Список возможных ходов
        :rtype: list[tuple]
        """

        move_set = []
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if not (i == 0 and j == 0):
                    if Engine.check_range(x + j, y + i) and (
                            board[y + i][x + j] == '--' or board[y + i][x + j][0] != color):
                        move_set.append((x + j, y + i))

        return move_set

    @staticmethod
    def check(board):
        """
        Проверка королей на шах.

        :param board: Матрица доски
        :type board: list[list[str]]
        :return: Словарь с результатами проверки
        """

        check_all = {
            'check_w': False,
            'check_b': False
        }
        for y in range(8):
            for x in range(8):
                chess_piece = board[y][x]
                if chess_piece[1] == 'K':

                    move_set = Engine.rook(x, y, chess_piece[0], board)
                    for move in move_set:
                        random_piece = board[move[1]][move[0]]
                        if random_piece[1] == 'R' or random_piece[1] == 'Q':
                            if random_piece[0] != chess_piece[0]:
                                check_all['check_' + chess_piece[0]] = True

                    move_set = Engine.bishop(x, y, chess_piece[0], board)
                    for move in move_set:
                        random_piece = board[move[1]][move[0]]
                        if random_piece[1] == 'B' or random_piece[1] == 'Q':
                            if random_piece[0] != chess_piece[0]:
                                check_all['check_' + chess_piece[0]] = True

                    move_set = Engine.knight(x, y, chess_piece[0], board)
                    for move in move_set:
                        random_piece = board[move[1]][move[0]]
                        if random_piece[1] == 'N':
                            if random_piece[0] != chess_piece[0]:
                                check_all['check_' + chess_piece[0]] = True

                    move_set = Engine.pawn(x, y, chess_piece[0], board)
                    for move in move_set:
                        random_piece = board[move[1]][move[0]]
                        if random_piece[1] == 'P':
                            if random_piece[0] != chess_piece[0]:
                                check_all['check_' + chess_piece[0]] = True

        return check_all

    @staticmethod
    def check_pawn_upgrade(x, y, board):
        """
        Проверяет, может ли пешка превратится в новую фигуру.

        :param x: X фигуры
        :type x: int
        :param y: Y фигуры
        :type y: int
        :param board: Матрица доски
        :type board: list[list[str]]
        :return: Результат проверки
        """

        x = int(x)
        y = int(y)
        if board[y][x][1] == 'P':
            if (y == 1 and board[y][x][0] == 'w') or (y == 6 and board[y][x][0] == 'b'):
                return True

        return False
