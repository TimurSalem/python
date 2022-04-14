from tkinter import *
from datetime import datetime as dt

WHITE = 1
BLACK = 2


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    return WHITE


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


class ChessPieces:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return None

    def can_move(self, board, row, col, row1, col1):
        return False

    def can_attack(self, board, row, col, row1, col1):
        return False


class Pawn(ChessPieces):
    def char(self):
        return '♟'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1 and board.field[row + direction][col] is None:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None
                and board.field[row + 2 * direction][col] is None):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Rook(ChessPieces):
    def char(self):
        return '♜'

    def can_move(self, board, row, col, row1, col1):

        if row != row1 and col != col1:
            return False

        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(row, c) is None):
                return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Knight(ChessPieces):

    def char(self):
        return '♞'

    def can_move(self, board, row, col, row1, col1):
        if 8 > row >= 0 and 8 > col >= 0:
            if abs(col1 - col) == 2 and abs(row1 - row) == 1 \
                    or abs(col1 - col) == 1 and abs(row1 - row) == 2:
                return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop(ChessPieces):
    def char(self):
        return '♝'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False

        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку

        if not (abs(row - row1) == abs(col - col1)):
            return False
        step_col = 1 if col1 > col else -1  # вправо влево
        step_row = 1 if row1 > row else -1  # вверх вниз
        r, c = row + step_row, col + step_col
        while r != row1 and c != col1:
            if board.get_piece(r, c) is not None:
                return False
            r += step_row
            c += step_col
        if not (board.get_piece(row1, col1) is None or
                board.get_piece(row1, col1).get_color() == opponent(self.color)):
            return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen(ChessPieces):
    def char(self):
        return '♛'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False

        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку

        if (row != row1 and col != col1) and \
                not (abs(row - row1) == abs(col - col1)):
            return False

        if row == row1 or col == col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                # Если на пути по вертикали есть фигура
                if not (board.get_piece(r, col) is None):
                    return False

            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1, step):
                # Если на пути по горизонтали есть фигура
                if not (board.get_piece(row, c) is None):
                    return False
        else:
            step_col = 1 if col1 > col else -1  # вправо влево
            step_row = 1 if row1 > row else -1  # вверх вниз
            r, c = row + step_row, col + step_col
            while r != row1 and c != col1:
                if board.get_piece(r, c) is not None:
                    return False
                r += step_row
                c += step_col
        if not (board.get_piece(row1, col1) is None or
                board.get_piece(row1, col1).get_color() == opponent(self.color)):
            return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King(ChessPieces):
    def char(self):
        return '♚'

    def can_move(self, board, row, col, row1, col1):
        if 8 > row1 >= 0 and 8 > col1 >= 0:
            if abs(row - row1) < 2 and abs(col - col1) < 2:
                return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), King(WHITE),
            Queen(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), King(BLACK),
            Queen(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        if self.field[row][col] is None:
            return ' '
        piece: ChessPieces = self.field[row][col]
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def who_win(self):
        blw = []
        whw = []

        for row in self.field:
            for col in row:
                if col.__class__.__name__ != 'NoneType':
                    blw.append(not (col.__class__.__name__ == 'King' and col.get_color() == WHITE))
                    whw.append(not (col.__class__.__name__ == 'King' and col.get_color() == BLACK))

        if all(blw):
            return BLACK
        elif all(whw):
            return WHITE
        else:
            return 'DRAW'

    def move_piece(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False"""

        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        if self.field[row][col] is None:
            return False
        piece: ChessPieces = self.field[row][col]
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = opponent(self.color)
        return True

    def get_piece(self, row, col):
        return self.field[row][col]


def main():
    from tkinter import font, Tk, Canvas, N, Button, CENTER
    W, H = 1000, 760

    x, y = 20, 20
    sx, sy = 3, 3
    selected = False
    color = ''
    nx = 1

    board = Board()

    root = Tk()
    root.title('♜♚~CHESS~♚♜')
    root.resizable(width=False, height=False)

    move_color = ''

    canvas = Canvas(root, bg='#547792', height=H, width=W,
                    highlightthickness=0)

    canvas.create_rectangle((13, 13), (747, 747), fill='#c6cdd7')
    canvas.create_rectangle((20, 20), (740, 740), fill='#fffcf9')
    canvas.create_rectangle((760, 13), (990, 747), fill='#fffcf9')
    canvas.create_rectangle((760, 13), (990, 43), fill='#af7656')
    # Luminari
    movecolor = canvas.create_text(875, 55, text='Ход белых',
                                   font=('Phosphate Solid', 35),
                                   fill='#1e1e28', anchor=N)
    moveright = canvas.create_text(875, 120, text='',
                                   font=('Phosphate Solid', 25),
                                   fill='#df4653')

    restart_button = Button(root, text='Заново', bg='#2a4b74',
                            highlightbackground='#2a4b74',
                            activeforeground='#eee9e8',
                            activebackground='#264b74', width=11,
                            height=2, fg='white',
                            font=('Phosphate Solid', 32))

    tm = canvas.create_text(875, 635, text='',
                            fill='#b9aea3', font=('Comic Sans MS', 20))
    canvas.create_text(880, 355,
                       text='  Очень уж много времени\n'
                            '        ушло на разроботку\n'
                            '          этиx шахмат не'
                            '\n      думал что это будет\n'
                            'настолько сложно где-то 28'
                            '\n      часов ушло на это\n'
                            'много времени ушло на отлов'
                            '\n     багов и построении\n'
                            '   красивого интерфейса,\n'
                            ' но думаю оно того стоило!\n'
                            'Я не знал чем заполнить это\n'
                            '    пространство и решил\n'
                            'это написать, сначала хотел\n'
                            '     сделать логи игры со \n'
                            'скролингом, но разбираться\n'
                            '        в этом было бы\n'
                            ' слишком скучно и долго!',
                       fill='#cdc6bb', font=('Comic Sans MS', 15))

    dt1 = dt.now()

    if not ('Phosphate' in font.families()):
        print(font.families())
        print('к сожалению у вас не установлен шрифт который я выбрал :(')
        print('Возможно у вас слетят все надписи со своих предусмотренных позиций')
        print('Сверху я любезно предоставил все шрифты которые есть на вашем компьютере')

    for j in range(8):
        for i in range(8):
            if i % 2 == 1:
                canvas.create_rectangle((x, y), (x + (720 // 8), y + (720 // 8)),
                                        fill='#010c10')
            x += 720 // 8

        y += 720 // 8
        x = 20 if j % 2 != 0 else -(720 // 8) + 20

    pack = {}

    for row in range(7, -1, -1):
        for col in range(8):
            if board.cell(row, col)[1:] != '':
                pack[f'{col} {row}'] = (canvas.create_text(col * 720 // 8 + 65, row * 720 // 8 + 60,
                                                           text=board.cell(row, col)[1:],
                                                           justify=CENTER,
                                                           font="Arial_Black 84",
                                                           fill='#d8cac4'
                                                           if board.cell(row, col)[0] == 'b'
                                                           else '#4d5a69'))

    def atack(row, col):
        nonlocal pack
        nonlocal selected
        nonlocal nx

        try:
            if f'{row} {col}' != f'{sy} {sx}':

                if board.move_piece(sx, sy, col, row):
                    canvas.coords(pack[f'{sy} {7 - sx}'],
                                  row * 720 // 8 + 65, (7 - col) * 720 // 8 + 60)
                    selected = False
                    canvas.itemconfigure(pack[f'{sy} {7 - sx}'], fill=color)
                    try:
                        canvas.delete(pack[f'{row} {7 - col}'])
                    except KeyError:
                        pass

                    pack[f'{row} {7 - col}'] = pack[f'{sy} {7 - sx}']
                    del pack[f'{sy} {7 - sx}']
                    nx += 1
                    canvas.itemconfigure(movecolor, text='Ход черных')

                    if nx > 2:
                        nx = 1
                        canvas.itemconfigure(movecolor, text='Ход белых')

                    if board.who_win() == BLACK:
                        canvas.itemconfigure(movecolor,
                                             text='    Черные\nвыиграли!')
                        dt2 = dt.now()
                        resd = dt2 - dt1
                        canvas.itemconfigure(tm, text='Игра длилась:'
                                                      + str(int(resd.total_seconds() // 60))
                                                      + ' мин')

                    elif board.who_win() == WHITE:
                        canvas.itemconfigure(movecolor,
                                             text='     Белые\nвыиграли!')
                        dt2 = dt.now()
                        resd = dt2 - dt1

                        canvas.itemconfigure(tm, text='Игра длилась: '
                                                      + str(int(resd.total_seconds() // 60))
                                                      + ' мин')

                else:
                    canvas.itemconfigure(moveright, text='Неверный ход!', fill='#df4653')

                    canvas.itemconfigure(pack[f'{sy} {7 - sx}'], fill=color)

                    selected = False
            else:
                canvas.itemconfigure(pack[f'{sy} {7 - sx}'], fill=color)

                selected = False

        except KeyError:
            selected = False

    def select_piece(event):
        x = event.x
        y = event.y
        nonlocal selected
        nonlocal sx
        nonlocal sy
        nonlocal color
        nonlocal nx
        nonlocal move_color

        canvas.itemconfigure(moveright, text='')

        if nx == 1:
            move_color = '#d8cac4'

        elif nx == 2:
            move_color = '#4d5a69'

        if 740 >= x >= 20 and 740 >= y >= 20:
            row = (x - 20) // (720 // 8)
            col = 7 - (y - 20) // (720 // 8)

            try:

                if not selected:
                    color = canvas.itemcget(pack[f'{row} {7 - col}'], 'fill')

                    if canvas.itemcget(pack[f'{row} {7 - col}'],
                                       'fill') == move_color:
                        canvas.itemconfigure(pack[f'{row} {7 - col}'],
                                             fill='#d4896a')
                        selected = True
                        sx = col
                        sy = row
                    else:
                        canvas.itemconfigure(moveright,
                                             text='не тот цвет')

                else:
                    atack(row, col)
            except KeyError:
                pass

    def check(event):
        if board.who_win() == 'DRAW':
            select_piece(event)

    def restart():
        nonlocal canvas
        nonlocal board
        nonlocal pack
        nonlocal move_color
        nonlocal nx
        nonlocal selected
        nonlocal dt1
        nonlocal tm
        from datetime import datetime as dt

        dt1 = dt.now()
        canvas.itemconfigure(tm, text='')

        for el in pack.values():
            canvas.delete(el)

        board = Board()
        canvas.itemconfigure(movecolor, text='Ход белых')
        nx = 1
        selected = False

        for row in range(7, -1, -1):
            for col in range(8):
                if board.cell(row, col)[1:] != '':
                    pack[f'{col} {row}'] = \
                        (canvas.create_text(col * 720 // 8 + 65,
                                            row * 720 // 8 + 60,
                                            text=board.cell(row, col)[1:],
                                            justify=CENTER,
                                            font="Arial_Black 84",
                                            fill='#d8cac4'
                                            if board.cell(row, col)[0] == 'b'
                                            else '#4d5a69'))

    root.bind('<Button-1>', check)

    restart_button['command'] = restart
    restart_button.pack()
    canvas.create_window((875, 695), window=restart_button)

    canvas.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
