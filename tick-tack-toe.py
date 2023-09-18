from tkinter import *
from time import sleep

# TODO : Restart
# TODO : Анимация в конце игры

import win32api
win32api.LoadKeyboardLayout('00000409',1)


class Field:
    def __init__(self, canvas):
        self.canvas = canvas
        self.canvas.create_rectangle(0, 0, 700, 700, fill='#e9bd74')
        self.background = PhotoImage(file='background.gif')
        self.canvas.create_image(50, 50, anchor=NW, image=self.background)


class Game_controller:
    def __init__(self, canvas):
        self.canvas = canvas
        self.cursor = self.canvas.create_rectangle(200, 200, 230, 230, fill='blue')
        self.cursor_pos_x = 200
        self.cursor_pos_y = 200
        self.player = 1
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-Up>', self.turn_up)
        self.canvas.bind_all('<KeyPress-Down>', self.turn_down)
        self.canvas.bind_all('<a>', self.turn_left)
        self.canvas.bind_all('<d>', self.turn_right)
        self.canvas.bind_all('<w>', self.turn_up)
        self.canvas.bind_all('<s>', self.turn_down)
        self.canvas.bind_all('<KeyPress-Return>', self.put_figure)
        self.canvas.bind_all('<space>', self.put_figure)

    def turn_left(self, evt):
        if ((evt.keysym == 'Left' and self.player % 2 == 1) or (evt.keysym == 'a' and self.player % 2 == 0)) \
                and self.cursor_pos_x - 200 > 0:
            self.cursor_pos_x -= 200
            self.canvas.move(self.cursor, -200, 0)

    def turn_right(self, evt):
        if ((evt.keysym == 'Right' and self.player % 2 == 1) or (evt.keysym == 'd' and self.player % 2 == 0)) \
                and self.cursor_pos_x + 200 < 601:
            self.cursor_pos_x += 200
            self.canvas.move(self.cursor, 200, 0)

    def turn_up(self, evt):
        if ((evt.keysym == 'Up' and self.player % 2 == 1) or (evt.keysym == 'w' and self.player % 2 == 0)) \
                and self.cursor_pos_y - 200 > 0:
            self.cursor_pos_y -= 200
            self.canvas.move(self.cursor, 0, -200)

    def turn_down(self, evt):
        if ((evt.keysym == 'Down' and self.player % 2 == 1) or (evt.keysym == 's' and self.player % 2 == 0)) \
                and self.cursor_pos_y + 200 < 601:
            self.cursor_pos_y += 200
            self.canvas.move(self.cursor, 0, 200)

    def put_figure(self, evt):
        if ((evt.keysym == 'Return' and self.player % 2 == 1) or (evt.keysym == 'space' and self.player % 2 == 0)):
            if Game_state.field[self.cursor_pos_y // 200 - 1][self.cursor_pos_x // 200 - 1] == '*':
                x = self.cursor_pos_x // 200 - 1
                y = self.cursor_pos_y // 200 - 1
                coord_x = self.cursor_pos_x - 150
                coord_y = self.cursor_pos_y - 150

                if self.player % 2 == 1:
                    figures.put_cross(x=coord_x, y=coord_y)
                    Game_state.field[y][x] = 'X'
                else:
                    figures.put_zero(x=coord_x, y=coord_y)
                    Game_state.field[y][x] = 'O'

                if gs.checker():
                    endgame(self.player)
                elif self.player == 9:
                    canvas.create_text(350, 340, text='НИЧЬЯ', fill='white', font=('Times', 80))

                self.player += 1


class Game_state:
    field = [['*' for i in range(3)] for j in range(3)]

    def vertical(self):
        for i in range(3):
            a = [Game_state.field[0][i], Game_state.field[1][i], Game_state.field[2][i]]
            if all(char == 'X' for char in a) or all(char == 'O' for char in a):
                return True
        return False

    def horizontal(self):
        for i in range(3):
            if all(char == 'X' for char in Game_state.field[i]) or all(char == 'O' for char in Game_state.field[i]):
                return True
        return False

    def diagonal(self):
        if (Game_state.field[0][0] == Game_state.field[1][1] and Game_state.field[0][0] == Game_state.field[2][2]) and Game_state.field[1][1] != '*':
            return True
        if (Game_state.field[0][2] == Game_state.field[1][1] and Game_state.field[0][2] == Game_state.field[2][0]) and Game_state.field[1][1] != '*':
            return True
        return False

    def checker(self):
        if self.vertical() or self.horizontal() or self.diagonal():
            return True
        return False


class Figures:
    def __init__(self, canvas):
        self.canvas = canvas
        self.cross = PhotoImage(file="cross.gif")
        self.zero = PhotoImage(file="zero.gif")

    def put_cross(self, x, y):
        self.canvas.create_image(x, y, anchor=NW, image=self.cross)

    def put_zero(self, x, y):
        self.canvas.create_image(x, y, anchor=NW, image=self.zero)


def endgame(player):
    if player % 2 == 1:
        canvas.create_text(350, 340, text='X победил', fill='white', font=('Times', 80))
    else:
        canvas.create_text(350, 340, text='O победил', fill='white', font=('Times', 80))


tk = Tk()
tk.title('Крестики - нолики')
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)

canvas = Canvas(tk, width=700, height=700, bd=0, highlightthickness=0)
canvas.pack()

f = Field(canvas)
cursor = Game_controller(canvas)
gs = Game_state()
figures = Figures(canvas)

tk.mainloop()