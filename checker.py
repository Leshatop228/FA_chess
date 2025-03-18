class Board1:
    def __init__(self):
        self.NONE = None
        self.move_count = 0

        # Словарь для доски шашек (a-h, ряды 1-8)
        self.markup = {
            'a': [Checker('white'), self.NONE, Checker('white'), self.NONE, self.NONE, Checker('black'), self.NONE, Checker('black')],
            'b': [self.NONE, Checker('white'), self.NONE, self.NONE, self.NONE, self.NONE, Checker('black'), self.NONE],
            'c': [Checker('white'), self.NONE, Checker('white'), self.NONE, self.NONE, Checker('black'), self.NONE, Checker('black')],
            'd': [self.NONE, Checker('white'), self.NONE, self.NONE, self.NONE, self.NONE, Checker('black'), self.NONE],
            'e': [Checker('white'), self.NONE, Checker('white'), self.NONE, self.NONE, Checker('black'), self.NONE, Checker('black')],
            'f': [self.NONE, Checker('white'), self.NONE, self.NONE, self.NONE, self.NONE, Checker('black'), self.NONE],
            'g': [Checker('white'), self.NONE, Checker('white'), self.NONE, self.NONE, Checker('black'), self.NONE, Checker('black')],
            'h': [self.NONE, Checker('white'), self.NONE, self.NONE, self.NONE, self.NONE, Checker('black'), self.NONE],
        }

    def draw_board(self):
        print("  a b c d e f g h")
        print("---------------------")
        for row in range(8, 0, -1):
            print(row, end="|")
            for col in 'abcdefgh':
                variable = self.markup[col][row - 1]
                if variable == self.NONE:
                    print(".", end=" ")
                else:
                    print(variable, end=" ")
            print("|", row)
        print("--------------------")
        print("  a b c d e f g h")

    def get_position(self, turn):
        while True:
            # user_input = input(f"Введите координаты фигуры :  {'белых' if turn == 'white' else 'черных'} (например, 'a2'): ")
            if turn == 'white':
                user_input = input(f'Введите координаты фигуры Белых, например (a,2) или undo (откат) : ')
            else:
                user_input = input(f'Введите координаты фигуры  Черных, например (a,2)  или undo (откат) : ')

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

    def move_figure(self, start, end, turn):
        start_col, start_row = start
        end_col, end_row = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')


        checker = self.markup[start_col][start_row - 1]
        if checker == self.NONE or checker.color != turn:
            print("Здесь нет вашей шашки.")
            return False

        if not checker.can_move((start_row, start_col), (end_row, end_col), self):
            print("Недопустимый ход.")
            return False


        target = self.markup[end_col][end_row - 1]
        if target != self.NONE:
            if target.color == checker.color:
                print("Нельзя съесть свою шашку.")
                return False

            jump_row = (start_row + end_row) // 2
            jump_col = chr((ord(start_col) + ord(end_col)) // 2)
            jumped_checker = self.markup[jump_col][jump_row - 1]
            if jumped_checker == self.NONE or jumped_checker.color == checker.color:
                print("Невозможно съесть шашку.")
                return False

            self.markup[jump_col][jump_row - 1] = self.NONE
            print(f"Шашка {jumped_checker} съедена.")

        self.markup[end_col][end_row - 1] = checker
        self.markup[start_col][start_row - 1] = self.NONE
        print(f"Ход выполнен: {start_col}{start_row} -> {end_col}{end_row}")
        return True

    def play(self):
        turn = 'white'
        while True:
            self.draw_board()
            print(f"Ход {'белых' if turn == 'white' else 'черных'}.")
            start = self.get_position(turn)
            end = self.get_position(turn)
            if self.move_figure(start, end, turn):
                turn = 'black' if turn == 'white' else 'white'


class Figure:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def can_move(self, start, end):
        pass


class Checker(Figure):
    def __init__(self, color):
        super().__init__("Checker", color)

    def __str__(self):
        return "W" if self.color == "white" else "B"

    def can_move(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end
        start_col_num = ord(start_col) - ord('a')
        end_col_num = ord(end_col) - ord('a')

        row_diff = end_row - start_row
        col_diff = end_col_num - start_col_num


        if self.color == 'white':
            if row_diff == 1 and abs(col_diff) == 1:
                return board.markup[end_col][end_row - 1] == board.NONE

            if row_diff == 2 and abs(col_diff) == 2:
                jump_row = (start_row + end_row) // 2
                jump_col = chr((ord(start_col) + ord(end_col)) // 2)
                jumped_checker = board.markup[jump_col][jump_row - 1]
                return jumped_checker != board.NONE and jumped_checker.color != self.color
        else:
            if row_diff == -1 and abs(col_diff) == 1:
                return board.markup[end_col][end_row - 1] == board.NONE

            if row_diff == -2 and abs(col_diff) == 2:
                jump_row = (start_row + end_row) // 2
                jump_col = chr((ord(start_col) + ord(end_col)) // 2)
                jumped_checker = board.markup[jump_col][jump_row - 1]
                return jumped_checker != board.NONE and jumped_checker.color != self.color
        return False


if __name__ == "__main__":
    board = Board1()
    board.play()
