from chessboard import Board as ChessBoard
from checker import Board1 as CheckersBoard

def main():
    print("Выберите игру:")
    print("1 - Шахматы")
    print("2 - Шашки")

    choice = input("Введите номер игры: ")

    if choice == "1":
        board = ChessBoard()
        board.Whose_move()
    elif choice == "2":
        board = CheckersBoard()
        board.play()
    else:
        print("Некорректный выбор.")

if __name__ == "__main__":
    main()
