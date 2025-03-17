class Board:
    """
    Класс, представляющий шахматную доску. Управляет состоянием доски, фигурами, ходами и историей игры.

    Атрибуты:
        NONE (None): Константа, обозначающая пустую клетку на доске.
        move_count (int): Счетчик ходов.
        history (list): Список ходов, хранящий объекты класса Move.
        markup (dict): Словарь, представляющий состояние доски. Ключи — буквы столбцов (a-h), значения — списки фигур или None.
    """


    def __init__(self):
        """
        Инициализирует шахматную доску, расставляя фигуры в начальные позиции.
        """


        self.NONE = None
        self.move_count = 0
        self.history = []
        self.markup = {
            'a': [Rook('white'), Magnet('white'), self.NONE, self.NONE, self.NONE, self.NONE, Magnet('black'), Rook('black')],
            'b': [Knight('white'), Pawn('white'), self.NONE, self.NONE, self.NONE, self.NONE, Pawn('black'), Knight('black')],
            'c': [Princess('white'), Pawn('white'), self.NONE, self.NONE, self.NONE, self.NONE, Pawn('black'), Princess('black')],
            'd': [Queen('white'), Pawn('white'), self.NONE, self.NONE, self.NONE, self.NONE, Pawn('black'), Queen('black')],
            'e': [King('white'), Pawn('white'), self.NONE, self.NONE, self.NONE, self.NONE, Pawn('black'), King('black')],
            'f': [Bishop('white'), Pawn('white'), self.NONE, self.NONE, self.NONE, self.NONE, Pawn('black'), Bishop('black')],
            'g': [Knight('white'), Pawn('white'), self.NONE, self.NONE, self.NONE, self.NONE, Pawn('black'), Knight('black')],
            'h': [Rook('white'), Kangaroo('white'), self.NONE, self.NONE, self.NONE, self.NONE, Kangaroo('black'), Rook('black')],
        }

    def draw_board(self):
        print("  a b c d e f g h")
        print("---------------------")
        for row in range(8, 0, -1):
            print(row, end="|")
            for col in 'abcdefgh':
                variable = self.markup[col][row - 1]
                if variable == None:
                    variable = "."
                    print(variable, end=" ")
                else:
                    print(variable, end=" ")
            print("|", row)
        print("--------------------")
        print("  a b c d e f g h")

    def move_figure(self, start, end):
        """
        Перемещает фигуру с начальной позиции на конечную.

        Параметры:
            start (tuple): Кортеж из двух элементов (str, int), представляющий начальную позицию фигуры.
            end (tuple): Кортеж из двух элементов (str, int), представляющий конечную позицию фигуры.

        Возвращает:
            bool: True, если ход выполнен успешно, иначе False.

        Исключения:
            None
        """

        start_col, start_row = start
        end_col, end_row = end
        point = self.markup[start_col][start_row - 1]
        target = self.markup[end_col][end_row - 1]

        if point == self.NONE:
            print("Фигуры тут нет")
            return False

        if not point.can_move((start_row, start_col), (end_row, end_col), self):
            print("Не допустимый ход")
            return False


        move = Move(start,end,point,target)
        self.history.append(move)



        if isinstance(point, Magnet):
            start_col_num = ord(start_col) - ord('a')
            end_col_num = ord(end_col) - ord('a')
            distance = max(abs(start_row - end_row), abs(start_col_num - end_col_num))

            if distance > 1 and target != self.NONE and self._is_enemy(point, target):
                row_step = 1 if start_row > end_row else -1 if start_row < end_row else 0
                col_step = 1 if start_col > end_col else -1 if start_col < end_col else 0
                new_row = end_row + row_step
                new_col = chr(ord(end_col) + col_step)

                if self.markup[new_col][new_row - 1] == self.NONE:
                    self.markup[new_col][new_row - 1] = target
                    self.markup[end_col][end_row - 1] = self.NONE
                    print(f"Фигура {target} притянута к {new_col}{new_row}")
                    self.move_count += 1
                    self.draw_board()
                    return True
                else:
                    print("Клетка для притягивания занята")
                    return False
        if isinstance(point, Princess):
            if target != self.NONE:
                if self._is_enemy(point, target):
                    if target.name == "Queen":
                        print("Принцесса не может съесть королеву!")
                        return False
                    if self.move_count % 2 == 0:  # Проверка на четный ход
                        print(f"Принцесса съела фигуру {target}")
                        self.markup[end_col][end_row - 1] = point
                        self.markup[start_col][start_row - 1] = self.NONE
                        self.move_count += 1
                        self.draw_board()
                        return True
                    else:
                        print("Принцесса может съедать фигуры только на четных ходах!")
                        return False
                else:
                    print("Вы пытаетесь съесть свою фигуру!")
                    return False

        if target != self.NONE:
            if self._is_enemy(point, target):
                print(f"Фигуру {target} съели")
            else:
                print("вы решили убить свою фигуру (партизан)")
                return False

        self.markup[end_col][end_row - 1] = point
        self.markup[start_col][start_row - 1] = self.NONE
        print(f"Ход выполнен успешно: {start_col}{start_row} -> {end_col}{end_row}")
        self.move_count += 1
        self.draw_board()
        return True

    def _is_enemy(self, figure1, figure2):
        """
        Проверяет, являются ли две фигуры врагами (разного цвета).

        Параметры:
            figure1 (Figure): Первая фигура.
            figure2 (Figure): Вторая фигура.

        Возвращает:
            bool: True, если фигуры враги, иначе False.
        """
        return figure1.color != figure2.color

    def undo_move(self, turn):
        """
        Откатывает последний ход и восстанавливает состояние доски.

        Параметры:
            turn (str): Очередь игрока ('white' или 'black').

        Возвращает:
            str: Очередь игрока после отката.
        """


        if not self.history:
            print("Нет ходов для отката")
            return turn

        last_move = self.history.pop()

        start_col, start_row = last_move.start
        end_col, end_row = last_move.end

        self.markup[start_col][start_row - 1] = last_move.point


        self.markup[end_col][end_row - 1] = last_move.target

        self.markup[last_move.end[0]][last_move.end[1] - 1] = self.NONE

        self.move_count -= 1

        print(f"Откат хода: {end_col}{end_row} -> {start_col}{start_row}")
        self.draw_board()

        if turn == 'white':
            turn = 'black'
        else:
            turn = 'white'
        return turn

    def Whose_move(self):
        """
        Основной игровой цикл, который поочередно запрашивает ходы у игроков.
        """


        turn = 'white'  # Начинают белые
        while True:
            if turn == 'white':
                print(f"Ход белых, сделано ходов: {self.move_count}")
            else:
                print(f"Ход черных, сделано ходов: {self.move_count}")

            self.draw_board()
            start = self.get_position(turn)
            if start == '':
                print("Игра завершена.")
                print(f"Всего сделано ходов: {self.move_count}")
                break


            end = self.get_position(turn)
            if end == '':
                print("Игра завершена.")
                print(f"Всего сделано ходов: {self.move_count}")
                break

            if self.move_figure(start, end):
                if turn == 'white':
                    turn = 'black'
                else:
                    turn = 'white'

    def get_position(self, turn):
        """
        Запрашивает у игрока координаты фигуры для хода.

        Параметры:
            turn (str): Очередь игрока ('white' или 'black').

        Возвращает:
            tuple: Кортеж из двух элементов (str, int), представляющий позицию фигуры.
        """


        while True:
            # user_input = input(f"Введите координаты фигуры :  {'белых' if turn == 'white' else 'черных'} (например, 'a2'): ")
            if turn == 'white':
                user_input = input(f'Введите координаты фигуры Белых, например (a,2) или undo (откат) : ')
            else:
                user_input = input(f'Введите координаты фигуры  Черных, например (a,2)  или undo (откат) : ')
            if user_input == 'undo':
                turn = self.undo_move(turn)
                continue


            if len(user_input) == 0:
                return ''
            if len(user_input) != 2:
                print('вы ввели неправильные координаты ')
                continue
            col = user_input[0]
            row = user_input[1]
            if col not in 'abcdefgh':
                print("столбец должен быть от 'a' до 'h'")
                continue
            if row not in '12345678':
                print("ряд должен быть от 1 до 8")
                continue
            return (col, int(row))


class Move:
    """
    Класс, представляющий ход фигуры.

    Атрибуты:
        start (tuple): Начальная позиция фигуры.
        end (tuple): Конечная позиция фигуры.
        point (Figure): Фигура, которая была перемещена.
        target (Figure): Фигура, которая была съедена (если есть).
    """


    def __init__(self, start, end, point, target):
        self.start = start
        self.end = end
        self.point = point
        self.target = target



class Figure:
    """
    Базовый класс для всех шахматных фигур.

    Атрибуты:
        name (str): Название фигуры.
        color (str): Цвет фигуры ('white' или 'black').

    Методы:
        can_move(start, end, board=None): Проверяет, может ли фигура переместиться с начальной позиции на конечную.
    """


    def __init__(self, name, color):
        self.name = name
        self.color = color



    def can_move(self, start, end):
        """
        Проверяет, может ли фигура переместиться с начальной позиции на конечную.

        Параметры:
            start (tuple): Кортеж из двух элементов (str, int), представляющий начальную позицию фигуры.
            end (tuple): Кортеж из двух элементов (str, int), представляющий конечную позицию фигуры.

        Возвращает:
            bool: True, если ход допустим, иначе False.
        """


        pass

class Pawn(Figure):
    """
    Класс, представляющий пешку.

    Наследуется от класса Figure и переопределяет метод can_move для реализации правил перемещения пешки.
    """


    def __init__(self, color):
        super().__init__("Pawn", color)



    def can_move(self, start, end, board=None):
        """
        Проверяет, может ли пешка переместиться с начальной позиции на конечную.

        Параметры:
            start (tuple): Кортеж из двух элементов (str, int), представляющий начальную позицию пешки.
            end (tuple): Кортеж из двух элементов (str, int), представляющий конечную позицию пешки.
            board (Board, опционально): Доска, на которой выполняется ход.

        Возвращает:
            bool: True, если ход допустим, иначе False.
        """


        start_row, start_col = start
        end_row, end_col = end

        if self.color == 'white':
            return (start_row + 1 == end_row and start_col == end_col) or (start_row == 1 and end_row == 3 and start_col == end_col)
        else:
            return (start_row - 1 == end_row and start_col == end_col) or (start_row == 6 and end_row == 4 and start_col == end_col)

    def __str__(self):
        """
        Магический метод, возвращающий строковое представление объекта.

        Возвращает:
            str: Строковое представление объекта.
        """


        return self.name[0]

class Rook(Figure):
    """
    Класс, представляющий ладью.

    Наследуется от класса Figure и переопределяет метод can_move для реализации правил перемещения ладьи.
    """


    def __init__(self, color):
        super().__init__('Rook', color)



    def can_move(self, start, end, board=None):
        """
        Проверяет, может ли ладья переместиться с начальной позиции на конечную.

        Параметры:
            start (tuple): Кортеж из двух элементов (str, int), представляющий начальную позицию ладьи.
            end (tuple): Кортеж из двух элементов (str, int), представляющий конечную позицию ладьи.
            board (Board, опционально): Доска, на которой выполняется ход.

        Возвращает:
            bool: True, если ход допустим, иначе False.
        """


        start_row, start_col = start
        end_row, end_col = end
        return start_row == end_row or start_col == end_col

    def __str__(self):
        """
        Магический метод, возвращающий строковое представление объекта.

        Возвращает:
            str: Строковое представление объекта.
        """


        return self.name[0]

class Bishop(Figure):
    """
    Класс, представляющий слона.

    Наследуется от класса Figure и переопределяет метод can_move для реализации правил перемещения слона.
    """


    def __init__(self, color):
        super().__init__('Bishop', color)


    def can_move(self, start, end, board=None):
        """
        Проверяет, может ли слон переместиться с начальной позиции на конечную.

        Параметры:
            start (tuple): Кортеж из двух элементов (str, int), представляющий начальную позицию слона.
            end (tuple): Кортеж из двух элементов (str, int), представляющий конечную позицию слона.
            board (Board, опционально): Доска, на которой выполняется ход.

        Возвращает:
            bool: True, если ход допустим, иначе False.
        """


        start_row, start_col = start
        end_row, end_col = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')
        return abs(start_row - end_row) == abs(start_col_num - end_col_num)

    def __str__(self):
        """
        Магический метод, возвращающий строковое представление объекта.

        Возвращает:
            str: Строковое представление объекта.
        """


        return self.name[0]

class Knight(Figure):
    """
    Класс, представляющий коня.

    Наследуется от класса Figure и переопределяет метод can_move для реализации правил перемещения коня.
    """
    def __init__(self, color):
        super().__init__('Knight', color)

    def can_move(self, start, end, board=None):
        """
        Проверяет, может ли король переместиться с начальной позиции на конечную.

        Параметры:
            start (tuple): Кортеж из двух элементов (str, int), представляющий начальную позицию короля.
            end (tuple): Кортеж из двух элементов (str, int), представляющий конечную позицию короля.
            board (Board, опционально): Доска, на которой выполняется ход.

        Возвращает:
            bool: True, если ход допустим, иначе False.
        """


        start_row, start_col = start
        end_row, end_col = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')
        return ((abs(start_row - end_row) == 2 and abs(start_col_num - end_col_num) == 1) or (abs(start_row - end_row) == 1 and abs(start_col_num - end_col_num) == 2))

    def __str__(self):
        """
        Магический метод, возвращающий строковое представление объекта.

        Возвращает:
            str: Строковое представление объекта.
        """


        return self.name[1]

class King(Figure):
    """
    Класс, представляющий короля.

    Наследуется от класса Figure и переопределяет метод can_move для реализации правил перемещения короля.
    """


    def __init__(self, color):
        super().__init__('King', color)



    def can_move(self, start, end, board=None):
        """
        Проверяет, может ли король переместиться с начальной позиции на конечную.

        Параметры:
            start (tuple): Кортеж из двух элементов (str, int), представляющий начальную позицию короля.
            end (tuple): Кортеж из двух элементов (str, int), представляющий конечную позицию короля.
            board (Board, опционально): Доска, на которой выполняется ход.

        Возвращает:
            bool: True, если ход допустим, иначе False
        """


        start_row, start_col = start
        end_row, end_col = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')
        return abs(start_row - end_row) <= 1 and abs(start_col_num - end_col_num) <= 1

    def __str__(self):
        """
        Магический метод, возвращающий строковое представление объекта.

        Возвращает:
            str: Строковое представление объекта.
        """


        return self.name[0]

class Queen(Figure):
    """
    Класс, представляющий ферзя.

    Наследуется от класса Figure и переопределяет метод can_move для реализации правил перемещения ферзя.
    """


    def __init__(self, color):
        super().__init__('Queen', color)



    def can_move(self, start, end, board=None):
        """
        Проверяет, может ли ферзь переместиться с начальной позиции на конечную.

        Параметры:
            start (tuple): Кортеж из двух элементов (str, int), представляющий начальную позицию ферзя.
            end (tuple): Кортеж из двух элементов (str, int), представляющий конечную позицию ферзя.
            board (Board, опционально): Доска, на которой выполняется ход.

        Возвращает:
            bool: True, если ход допустим, иначе False.
        """


        start_row, start_col = start
        end_row, end_col = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')

        if start_row == end_row or start_col_num == end_col_num:
            return True
        elif abs(start_row - end_row) == abs(start_col_num - end_col_num):
            return True
        else:
            return False

    def __str__(self):
        """
        Магический метод, возвращающий строковое представление объекта.

        Возвращает:
            str: Строковое представление объекта.
        """


        return self.name[0]

class Magnet(Figure):
    """
    Класс, представляющий магнит.

    Наследуется от класса Figure и переопределяет метод can_move для реализации правил перемещения магнита.
    """


    def __init__(self, color):
        super().__init__("Magnet", color)



    def can_move(self, start, end, board=None):
        """
        Проверяет, может ли магнит переместиться с начальной позиции на конечную.

        Параметры:
            start (tuple): Кортеж из двух элементов (str, int), представляющий начальную позицию магнита.
            end (tuple): Кортеж из двух элементов (str, int), представляющий конечную позицию магнита.
            board (Board, опционально): Доска, на которой выполняется ход.

        Возвращает:
            bool: True, если ход допустим, иначе False.
        """


        start_row, start_col = start
        end_row, end_col = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')

        if abs(start_row - end_row) <= 1 and abs(start_col_num - end_col_num) <= 1:
            return True

        if board is not None:
            row_diff = abs(start_row - end_row)
            col_diff = abs(start_col_num - end_col_num)
            if (row_diff == 0 or col_diff == 0 or row_diff == col_diff) and max(row_diff, col_diff) <= 5:
                target = board.markup[end_col][end_row - 1]
                if target != board.NONE and target.color != self.color:
                    return True
                else:
                    return False

    def __str__(self):
        """
        Магический метод, возвращающий строковое представление объекта.

        Возвращает:
            str: Строковое представление объекта.
        """


        return self.name[0]

class Kangaroo(Figure):
    """
    Класс, представляющий кенгуру.

    Наследуется от класса Figure и переопределяет метод can_move для реализации правил перемещения кенгуру.
    """


    def __init__(self, color):
        super().__init__("Kangaroo", color)



    def can_move(self, start, end, board=None):
        """
        Проверяет, может ли кенгуру переместиться с начальной позиции на конечную.

        Параметры:
            start (tuple): Кортеж из двух элементов (str, int), представляющий начальную позицию кенгуру.
            end (tuple): Кортеж из двух элементов (str, int), представляющий конечную позицию кенгуру.
            board (Board, опционально): Доска, на которой выполняется ход.

        Возвращает:
            bool: True, если ход допустим, иначе False.
        """


        start_row, start_col = start
        end_row, end_col = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')


        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col_num - end_col_num)

        if (row_diff == 3 and col_diff == 0) or (row_diff == 0 and col_diff == 3) or  (row_diff == 3 and col_diff == 3):
            return True
        else:
            return False

    def __str__(self):
        """
        Магический метод, возвращающий строковое представление объекта.

        Возвращает:
            str: Строковое представление объекта.
        """


        return self.name[1]


class Princess(Figure):
    """
    Класс, представляющий принцессу.

    Наследуется от класса Figure и переопределяет метод can_move для реализации правил перемещения принцессы.
    """


    def __init__(self, color):
        super().__init__("Princess", color)
        self.has_eaten = False

        def can_eat_enemy(self, target):
            """Проверяет, может ли принцесса съесть фигуру"""
            if self.has_eaten:
                return False
            elif target is None:
                return False
            elif target.color == self.color:
                return False
            elif target.name == "Queen":
                return False
            else:
                return True

    def can_move_like_king(self, start_row, start_col_num, end_row, end_col_num):
        """Проверяет, может ли принцесса пойти на 1 клетку"""


        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col_num - end_col_num)
        return row_diff <= 1 and col_diff <= 1

    def can_move(self, start, end, board=None):
        """
        Проверяет, может ли принцесса переместиться с начальной позиции на конечную.

        Параметры:
            start (tuple): Кортеж из двух элементов (str, int), представляющий начальную позицию принцессы.
            end (tuple): Кортеж из двух элементов (str, int), представляющий конечную позицию принцессы.
            board (Board, опционально): Доска, на которой выполняется ход.

        Возвращает:
            bool: True, если ход допустим, иначе False.
        """


        start_row, start_col = start
        end_row, end_col = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')
        target = board.markup[end_col][end_row - 1]


        if self.can_eat_enemy(target):
            return True


        if self.has_eaten == True:
            if board.move_count % 2 == 0:
                if self.can_move_like_king(start_row, start_col_num, end_row, end_col_num):
                    return True

        return False

    def __str__(self):
        """
        Магический метод, возвращающий строковое представление объекта.

        Возвращает:
            str: Строковое представление объекта.
        """


        return self.name[2]


board = Board()

if __name__ == "__main__":
    print("Доска до хода:")
    board.draw_board()

    game = board.Whose_move()
