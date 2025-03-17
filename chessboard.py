class Board:
    """Chess board that manages the board state, pieces, moves, and game history.

    Attributes:
        NONE (None): Constant representing an empty square on the board.
        move_count (int): Counter for moves.
        history (list): List of Move objects representing the move history.
        markup (dict): Dictionary representing the board state. Keys are column letters ('a'-'h') and values are lists of pieces or None.
    """

    def __init__(self):
        """Initializes the chess board with the starting positions."""

        self.NONE = None
        self.move_count = 0
        self.history = []
        self.markup = {
            'a': [Rook('white'), Magnet('white'), self.NONE, self.NONE, self.NONE, self.NONE, Magnet('black'),
                  Rook('black')],
            'b': [Knight('white'), Pawn('white'), self.NONE, self.NONE, self.NONE, self.NONE, Pawn('black'),
                  Knight('black')],
            'c': [Princess('white'), Pawn('white'), self.NONE, self.NONE, self.NONE, self.NONE, Pawn('black'),
                  Princess('black')],
            'd': [Queen('white'), Pawn('white'), self.NONE, self.NONE, self.NONE, self.NONE, Pawn('black'),
                  Queen('black')],
            'e': [King('white'), Pawn('white'), self.NONE, self.NONE, self.NONE, self.NONE, Pawn('black'),
                  King('black')],
            'f': [Bishop('white'), Pawn('white'), self.NONE, self.NONE, self.NONE, self.NONE, Pawn('black'),
                  Bishop('black')],
            'g': [Knight('white'), Pawn('white'), self.NONE, self.NONE, self.NONE, self.NONE, Pawn('black'),
                  Knight('black')],
            'h': [Rook('white'), Kangaroo('white'), self.NONE, self.NONE, self.NONE, self.NONE, Kangaroo('black'),
                  Rook('black')],
        }

    def draw_board(self):
        """Prints the board to the console in a formatted layout."""
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
        """Moves a piece from the starting position to the ending position.

        Args:
            start (tuple): A tuple (str, int) representing the piece's starting position.
            end (tuple): A tuple (str, int) representing the piece's ending position.

        Returns:
            bool: True if the move was successful, otherwise False.
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

        move = Move(start, end, point, target)
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
        """Checks whether two pieces are enemies (of different colors).

        Args:
            figure1 (Figure): The first piece.
            figure2 (Figure): The second piece.

        Returns:
            bool: True if the pieces are enemies, otherwise False.
        """
        return figure1.color != figure2.color

    def undo_move(self, turn):
        """Reverts the last move and restores the board state.

        Args:
            turn (str): The current player's turn ('white' or 'black').

        Returns:
            str: The player's turn after undoing the move.
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
        """Main game loop that alternately requests moves from the players."""

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
        """Prompts the player to input the coordinates of the piece to move.

        Args:
            turn (str): The player's turn ('white' or 'black').

        Returns:
            tuple: A tuple (str, int) representing the piece's position.
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
    """Represents a move of a chess piece.

    Attributes:
        start (tuple): The starting position of the piece.
        end (tuple): The ending position of the piece.
        point (Figure): The piece that was moved.
        target (Figure): The piece that was captured (if any).
    """

    def __init__(self, start, end, point, target):
        self.start = start
        self.end = end
        self.point = point
        self.target = target


class Figure:
    """Base class for all chess pieces.

    Attributes:
        name (str): The name of the piece.
        color (str): The color of the piece ('white' or 'black').

    Methods:
        can_move(start, end, board=None): Checks if the piece can move from the starting position to the ending position.
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
    """Represents a pawn.

    Inherits from Figure and overrides the can_move method to implement pawn movement rules.
    """

    def __init__(self, color):
        super().__init__("Pawn", color)

    def can_move(self, start, end, board=None):
        """Checks if the pawn can move from the starting position to the ending position.

        Args:
            start (tuple): A tuple (str, int) representing the pawn's starting position.
            end (tuple): A tuple (str, int) representing the pawn's ending position.
            board (Board, optional): The board on which the move is being made.

        Returns:
            bool: True if the move is valid, otherwise False.
        """

        start_row, start_col = start
        end_row, end_col = end

        if self.color == 'white':
            return (start_row + 1 == end_row and start_col == end_col) or (
                    start_row == 1 and end_row == 3 and start_col == end_col)
        else:
            return (start_row - 1 == end_row and start_col == end_col) or (
                    start_row == 6 and end_row == 4 and start_col == end_col)

    def __str__(self):
        """Returns the string representation of the pawn.

        Returns:
            str: The first letter of the pawn's name.
        """

        return self.name[0]


class Rook(Figure):
    """Represents a rook.

    Inherits from Figure and overrides the can_move method to implement rook movement rules.
    """

    def __init__(self, color):
        super().__init__('Rook', color)

    def can_move(self, start, end, board=None):
        """Checks if the rook can move from the starting position to the ending position.

        Args:
            start (tuple): A tuple (str, int) representing the rook's starting position.
            end (tuple): A tuple (str, int) representing the rook's ending position.
            board (Board, optional): The board on which the move is being made.

        Returns:
            bool: True if the move is valid, otherwise False.
        """

        start_row, start_col = start
        end_row, end_col = end
        return start_row == end_row or start_col == end_col

    def __str__(self):
        """Returns the string representation of the rook.

        Returns:
            str: The first letter of the rook's name.
        """

        return self.name[0]


class Bishop(Figure):
    """Represents a bishop.

    Inherits from Figure and overrides the can_move method to implement bishop movement rules.
    """

    def __init__(self, color):
        super().__init__('Bishop', color)

    def can_move(self, start, end, board=None):
        """Checks if the bishop can move from the starting position to the ending position.

        Args:
            start (tuple): A tuple (str, int) representing the bishop's starting position.
            end (tuple): A tuple (str, int) representing the bishop's ending position.
            board (Board, optional): The board on which the move is being made.

        Returns:
            bool: True if the move is valid, otherwise False.
        """

        start_row, start_col = start
        end_row, end_col = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')
        return abs(start_row - end_row) == abs(start_col_num - end_col_num)

    def __str__(self):
        """Returns the string representation of the bishop.

        Returns:
            str: The first letter of the bishop's name.
        """

        return self.name[0]


class Knight(Figure):
    """Represents a knight.

    Inherits from Figure and overrides the can_move method to implement knight movement rules.
    """

    def __init__(self, color):
        super().__init__('Knight', color)

    def can_move(self, start, end, board=None):
        """Checks if the knight can move from the starting position to the ending position.

        Args:
            start (tuple): A tuple (str, int) representing the knight's starting position.
            end (tuple): A tuple (str, int) representing the knight's ending position.
            board (Board, optional): The board on which the move is being made.

        Returns:
            bool: True if the move is valid, otherwise False.
        """

        start_row, start_col = start
        end_row, end_col = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')
        return ((abs(start_row - end_row) == 2 and abs(start_col_num - end_col_num) == 1) or (
                abs(start_row - end_row) == 1 and abs(start_col_num - end_col_num) == 2))

    def __str__(self):
        """Returns the string representation of the knight.

        Returns:
            str: The second letter of the knight's name.
        """
        return self.name[1]


class King(Figure):
    """Represents a king.

    Inherits from Figure and overrides the can_move method to implement king movement rules.
    """

    def __init__(self, color):
        super().__init__('King', color)

    def can_move(self, start, end, board=None):
        """Checks if the king can move from the starting position to the ending position.

        Args:
            start (tuple): A tuple (str, int) representing the king's starting position.
            end (tuple): A tuple (str, int) representing the king's ending position.
            board (Board, optional): The board on which the move is being made.

        Returns:
            bool: True if the move is valid, otherwise False.
        """
        start_row, start_col = start
        end_row, end_col = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')
        return abs(start_row - end_row) <= 1 and abs(start_col_num - end_col_num) <= 1

    def __str__(self):
        """Returns the string representation of the king.

        Returns:
            str: The first letter of the king's name.
        """
        return self.name[0]


class Queen(Figure):
    """Represents a queen.

    Inherits from Figure and overrides the can_move method to implement queen movement rules.
    """

    def __init__(self, color):
        super().__init__('Queen', color)

    def can_move(self, start, end, board=None):
        """Checks if the queen can move from the starting position to the ending position.

        Args:
            start (tuple): A tuple (str, int) representing the queen's starting position.
            end (tuple): A tuple (str, int) representing the queen's ending position.
            board (Board, optional): The board on which the move is being made.

        Returns:
            bool: True if the move is valid, otherwise False.
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
        """Returns the string representation of the queen.

        Returns:
            str: The first letter of the queen's name.
        """
        return self.name[0]


class Magnet(Figure):
    """Represents a magnet.

    Inherits from Figure and overrides the can_move method to implement magnet movement rules.
    """

    def __init__(self, color):
        super().__init__("Magnet", color)

    def can_move(self, start, end, board=None):
        """Checks if the magnet can move from the starting position to the ending position.

        Args:
            start (tuple): A tuple (str, int) representing the magnet's starting position.
            end (tuple): A tuple (str, int) representing the magnet's ending position.
            board (Board, optional): The board on which the move is being made.

        Returns:
            bool: True if the move is valid, otherwise False.
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
        """Returns the string representation of the magnet.

        Returns:
            str: The first letter of the magnet's name.
        """
        return self.name[0]


class Kangaroo(Figure):
    """Represents a kangaroo.

    Inherits from Figure and overrides the can_move method to implement kangaroo movement rules.
    """

    def __init__(self, color):
        super().__init__("Kangaroo", color)

    def can_move(self, start, end, board=None):
        """Checks if the kangaroo can move from the starting position to the ending position.

        Args:
            start (tuple): A tuple (str, int) representing the kangaroo's starting position.
            end (tuple): A tuple (str, int) representing the kangaroo's ending position.
            board (Board, optional): The board on which the move is being made.

        Returns:
            bool: True if the move is valid, otherwise False.
        """
        start_row, start_col = start
        end_row, end_col = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')

        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col_num - end_col_num)

        if (row_diff == 3 and col_diff == 0) or (row_diff == 0 and col_diff == 3) or (row_diff == 3 and col_diff == 3):
            return True
        else:
            return False

    def __str__(self):
        """Returns the string representation of the kangaroo.

        Returns:
            str: The second letter of the kangaroo's name.
        """
        return self.name[1]


class Princess(Figure):
    """Represents a princess.

    Inherits from Figure and overrides the can_move method to implement princess movement rules.
    """

    def __init__(self, color):
        super().__init__("Princess", color)
        self.has_eaten = False

    def can_eat_enemy(self, target):
        """Checks if the princess can capture an enemy piece."""
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
        """Checks if the princess can move like a king (one square in any direction)."""
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col_num - end_col_num)
        return row_diff <= 1 and col_diff <= 1

    def can_move(self, start, end, board=None):
        """Checks if the princess can move from the starting position to the ending position.

        Args:
            start (tuple): A tuple (str, int) representing the princess's starting position.
            end (tuple): A tuple (str, int) representing the princess's ending position.
            board (Board, optional): The board on which the move is being made.

        Returns:
            bool: True if the move is valid, otherwise False.
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
        """Returns the string representation of the princess.

        Returns:
            str: The third letter of the princess's name.
        """
        return self.name[2]


board = Board()

if __name__ == "__main__":
    print("Доска до хода:")
    board.draw_board()

    game = board.Whose_move()
