import random
import re
from PIL import Image, ImageDraw
from pathlib import Path

All_Battle = {}
path = Path("images", "field.jpg")

class Battle():
    counter = 0 # Счетчик для отслеживания количества созданных объектов

    """
    Инициализация объекта класса Battle.Устанавливает идентификаторы
    пользователя и оппонента, создает поле битвы, размещает
    корабли на поле в случайном порядке.
    """
    def __init__(self, tg_id, opp_id):
        Battle.counter += 1 # Увеличение счетчика при создании нового объекта
        self.id = Battle.counter # Установка идентификатора объекта
        self.id_user = tg_id  # Идентификатор пользователя
        self.id_opponent = opp_id # Идентификатор оппонента
        self.field = [[False] * 10 for _ in range(10)] # Поле битвы, изначально пустое
        self.ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Длина каждого корабля
        self.dict_ship = {}
        self.shots_fired = [[None] * 10 for _ in range(10)]  # Координаты, куда мы стреляли и попали или не попали
        self.enemy_shots = [[None] * 10 for _ in range(10)]  # Координаты, куда в нас стреляли и попали или не попали

        # Размещение кораблей на поле в случайном порядке
        for ship_length in self.ships:
            while True:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                orientation = random.choice(['horizontal', 'vertical'])

                if self.can_place_ship(x, y, ship_length, orientation):
                    self.place_ship(x, y, ship_length, orientation)
                    break


    #def hurt_or_kill(self, x, y):



    """
    Проверяет возможность размещения корабля заданной длины и 
    ориентации на указанных координатах (x, y). 
    Возвращает True, если размещение возможно, иначе False.
    """
    def can_place_ship(self, x, y, ship_length, orientation):
        if orientation == 'horizontal':
            if y + ship_length > 10:
                return False
            for i in range(ship_length):
                if self.field[x][y + i]:
                    return False
                if x > 0 and self.field[x - 1][y + i]:
                    return False
                if x < 9 and self.field[x + 1][y + i]:
                    return False
            if y > 0 and self.field[x][y - 1]:
                return False
            if y + ship_length < 10 and self.field[x][y + ship_length]:
                return False
        else:  # orientation == 'vertical'
            if x + ship_length > 10:
                return False
            for i in range(ship_length):
                if self.field[x + i][y]:
                    return False
                if y > 0 and self.field[x + i][y - 1]:
                    return False
                if y < 9 and self.field[x + i][y + 1]:
                    return False
            if x > 0 and self.field[x - 1][y]:
                return False
            if x + ship_length < 10 and self.field[x + ship_length][y]:
                return False
        return True

    """
    Размещает корабль заданной длины и ориентации на указанных координатах (x, y) на поле.
    """

    def place_ship(self, x, y, ship_length, orientation):
        coordinates = []  # Список для хранения координат текущего корабля

        if orientation == 'horizontal':
            for i in range(ship_length):
                self.field[x][y + i] = True
                coordinates.append([x, y + i])
        else:  # orientation == 'vertical'
            for i in range(ship_length):
                self.field[x + i][y] = True
                coordinates.append([x + i, y])

        # Проверяем, есть ли уже корабль такой длины в словаре dict_ship
        if ship_length in self.dict_ship:
            self.dict_ship[ship_length].append(coordinates)  # Добавляем координаты к существующему кораблю
        else:
            self.dict_ship[ship_length] = [coordinates]  # Создаем новую запись в словаре для данной длины корабля

    """
    Возвращает значение ячейки поля по указанным координатам.
    """
    def get_coordinate_value(self, coordinate):
        return self.field[coordinate[0]][coordinate[1]]

    """
    Выполняет выстрел игрока в указанные координаты. 
    Обновляет информацию о выстреле в соответствующей ячейке поля. 
    Возвращает True, если выстрел попал в корабль, иначе False.
    """
    def fire_at_coordinate(self, coordinate):
        letters = 'ABCDEFGHIJ'
        match = re.match(r"([А-Яа-я]+)(\d+)", coordinate)
        if match:
            letter = match.group(1)
            number = match.group(2)

        y = letters.index(letter)
        x = int(number) - 1
        if self.field[x][y]:
            self.shots_fired[x][y] = True
            return True
        else:
            self.shots_fired[x][y] = False
            return False

    """
    Получает выстрел оппонента в указанные координаты. 
    Обновляет информацию о выстреле оппонента в соответствующей ячейке поля. 
    Возвращает True, если выстрел попал в корабль нашего игрока, иначе False.
    """
    def receive_enemy_fire(self, coordinate):
        letters = 'ABCDEFGHIJ'
        match = re.match(r"([A-Za-z]+)(\d+)", coordinate)
        if match:
            letter = match.group(1)
            number = match.group(2)
            y = letters.index(letter)
            x = int(number) - 1
            if self.field[x][y]:
                self.enemy_shots[x][y] = True
                return True
            else:
                self.enemy_shots[x][y] = False
                return False
        return False


    """
    Проверяет остались ли на поле живые корабли, 
    которые не были поражены выстрелами оппонента. 
    Возвращает True, если есть живые корабли, иначе False.
    """
    def check_ships_alive(self):
        for i, row in enumerate(self.field):
            for j, cell in enumerate(row):
                if cell and not self.enemy_shots[i][j]:
                    return True
        return False

    def hurt_or_kill(self, coordinate):
        letters = 'ABCDEFGHIJ'
        match = re.match(r"([A-Za-z]+)(\d+)", coordinate)
        if match:
            letter = match.group(1)
            number = match.group(2)
            y = letters.index(letter)
            x = int(number) - 1
            for ship_length, ship_coordinates in self.dict_ship.items():
                for coordinates in ship_coordinates:
                    if [x, y] in coordinates:
                        coordinates.remove([x, y])  # Удаляем попадание из координат корабля
                        if len(coordinates) == 0:
                            #del self.dict_ship[ship_length]  # Если координаты пустые, значит корабль убит

                            return "kill"
                        else:
                            return "hurt"
            return "miss"  # Промах, координаты не принадлежат ни одному кораблю

    def add_ships_to_battlefield(self):
        # Открытие существующего изображения поля боя
        image = Image.open(path)
        draw = ImageDraw.Draw(image)

        cell_size = image.width // 10  # Вычисление размера клетки на изображении

        # Отрисовка кораблей и пометок
        for x in range(10):
            for y in range(10):
                if self.field[x][y]:
                    # Если клетка содержит корабль, отрисовываем его
                    draw.rectangle(
                        [(y * cell_size, x * cell_size), ((y + 1) * cell_size, (x + 1) * cell_size)],
                        fill="blue"
                    )
                if self.enemy_shots[x][y]:
                    # Если клетка была подстрелена, отрисовываем попадание красным цветом
                    draw.line(
                        [(y * cell_size, x * cell_size), ((y + 1) * cell_size, (x + 1) * cell_size)],
                        fill="red",
                        width=5
                    )
                    draw.line(
                        [((y + 1) * cell_size, x * cell_size), (y * cell_size, (x + 1) * cell_size)],
                        fill="red",
                        width=5
                    )
                elif self.enemy_shots[x][y] == False:
                    # Нарисовать точку в месте, куда не попали
                    point_size = 2  # Устанавливаем размер точки
                    point_position = (
                    (y + 0.5) * cell_size, (x + 0.5) * cell_size)  # Вычисляем координаты центра клетки
                    point_coords = (
                        int(point_position[0] - point_size // 2),
                        int(point_position[1] - point_size // 2),
                        int(point_position[0] + point_size // 2),
                        int(point_position[1] + point_size // 2)
                    )
                    draw.rectangle(point_coords, fill="red", width=25)

        # Отрисовка клеточной сетки
        for x in range(11):
            line_start = (0, x * cell_size)
            line_end = (image.width, x * cell_size)
            draw.line([line_start, line_end], fill="black")

        for y in range(11):
            line_start = (y * cell_size, 0)
            line_end = (y * cell_size, image.height)
            draw.line([line_start, line_end], fill="black")

        # Сохранение изображения с добавленными клетками и кораблями
        image.save('images/game' + str(self.id_user) + str(self.id_opponent) + 'see_battle.png', 'PNG')