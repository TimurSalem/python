WHITE = 1
BLACK = 2


def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


class BasicChessPiece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def get_color(self):
        return self.color

    def can_move(self, row1, col1):
        return row1 + col1


class Knight(BasicChessPiece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    @staticmethod
    def char():
        return 'N'

    def can_move(self, row, col):
        if 8 > row >= 0 and 8 > col >= 0:
            if abs(self.col - col) == 2 and abs(self.row - row) == 1 \
                    or abs(self.col - col) == 1 and abs(self.row - row) == 2:
                return True
        return False


class Rook(BasicChessPiece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    @staticmethod
    def char():
        return 'R'

    def can_move(self, row, col):
        if self.row != row and self.col != col:
            return False
        return True


class Bishop(BasicChessPiece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    @staticmethod
    def char():
        return 'B'

    def can_move(self, row, col):
        if 8 > row >= 0 and 8 > col >= 0:  # Проверка что обозначенный ход не выходит за границы поля
            if abs(col - self.col) == abs(row - self.row):
                return True
        return False


class Queen(BasicChessPiece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    @staticmethod
    def char():
        return 'Q'

    def can_move(self, row, col):
        if 8 > row >= 0 and 8 > col >= 0:  # Проверка что обозначенный ход не выходит за границы поля
            if abs(col - self.col) == abs(row - self.row) or row == self.row or col == self.col:
                return True
        return False


class King(BasicChessPiece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    @staticmethod
    def char():
        return 'K'

    def can_move(self, row, col):
        if 8 > row >= 0 and 8 > col >= 0:  # Проверка что обозначенный ход не выходит за границы поля
            if abs(row - self.row) < 2 and abs(col - self.col) < 2:
                return True
        return False


class Pawn(BasicChessPiece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)

    @staticmethod
    def char():
        return 'P'

    def can_move(self, row, col):
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        if self.row + direction == row:
            return True

        if self.row == start_row and self.row + 2 * direction == row:
            return True
        return False


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for _ in range(8):
            self.field.append([None] * 8)

        self.field[1] = [Pawn(1, 0, WHITE),
                         Pawn(1, 1, WHITE),
                         Pawn(1, 2, WHITE),
                         Pawn(1, 3, WHITE),
                         Pawn(1, 4, WHITE),
                         Pawn(1, 5, WHITE),
                         Pawn(1, 6, WHITE),
                         Pawn(1, 7, WHITE)]

        self.field[6] = [Pawn(6, 0, BLACK),
                         Pawn(6, 1, BLACK),
                         Pawn(6, 2, BLACK),
                         Pawn(6, 3, BLACK),
                         Pawn(6, 4, BLACK),
                         Pawn(6, 5, BLACK),
                         Pawn(6, 6, BLACK),
                         Pawn(6, 7, BLACK)]

        self.field[0] = [Rook(0, 0, WHITE),
                         Knight(0, 1, WHITE),
                         Bishop(0, 2, WHITE),
                         Queen(0, 3, WHITE),
                         King(0, 4, WHITE),
                         Bishop(0, 5, WHITE),
                         Knight(0, 6, WHITE),
                         Rook(0, 7, WHITE)]

        self.field[7] = [Rook(7, 0, BLACK),
                         Knight(7, 1, BLACK),
                         Bishop(7, 2, BLACK),
                         King(7, 3, BLACK),
                         Queen(7, 4, BLACK),
                         Bishop(7, 5, BLACK),
                         Knight(7, 6, BLACK),
                         Rook(7, 7, BLACK)]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def move_piece(self, row, col, row1, col1):

        rows = [row, row1]
        cols = [col, col1]
        if row - row1 == 0 or col - col1 == 0:
            sp = [self.field[r][c].__class__.__name__ != 'NoneType' for r, c in
                  zip(range(min(rows), max(rows)), range(min(cols), max(cols)))]
        else:
            sp = [(self.field[r][c].__class__.__name__ != 'NoneType' and
                   self.field[r][c].__class__.__name__ != self.field[row][col].__class__.__name__)
                  if abs(row - r) == abs(col - c)
                  else False for r, c in zip(range(min(rows), max(rows)),
                                             range(min(cols), max(cols)))]

        if any(sp) and self.field[row][col].__class__.__name__ != 'Knight':
            return False

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку

        piece: BasicChessPiece = self.field[row][col]

        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False

        if not piece.can_move(row1, col1):
            return False

        if piece.__class__.__name__ == 'Pawn' and col1 != col:
            if (self.field[row1][col1].__class__.__name__ == 'NoneType'
                    and abs(row1 - row) >= 2 and abs(col1 - col) >= 2):
                return False

        usl: BasicChessPiece = self.field[row1][col1]

        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        piece.set_position(row1, col1)
        self.color = opponent(self.color)

        if usl:
            name = usl.__class__.__name__ + ' ' + str(usl.color)
            return name
        return True


def print_board(board):  # Распечатать доску в текстовом виде
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def main():
    log = []
    board = Board()
    game_continue = True
    while game_continue:
        print_board(board)
        print('''Команды:
                 exit                               -- выход)
                 move <row> <col> <row1> <col1>     -- ход из клетки (row, col))
                                                       в клетку (row1, col1)''')
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход черных:')
        command = input()
        if command == 'exit':
            break

        log.append('Белые:' if board.current_player_color() == WHITE else 'Черные:' + command)
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        usl = board.move_piece(row, col, row1, col1)
        if usl:
            print('Ход успешен')
            if usl.__class__.__name__ == 'str':
                usl = usl.split()
                name = usl[0]
                color = usl[1]
                if color == '1':
                    color = 'White'
                else:
                    color = 'Black'

                usl = f'{color} {name}'

                print(f'Фигура {usl} была взята')

                if color:
                    color = 'чёрные'
                else:
                    color = 'белые'

                if name == 'King':
                    print(f'Игра закночена выиграли {color}')

        else:
            print('Координаты некорректы! Попробуйте другой ход!')

    for el in log:
        print(el)


if __name__ == '__main__':
    main()
