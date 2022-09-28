from tkinter import *
import generate_sudoku

GAP = 10
SHIFT = 50
valid_val = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


class point:
    value: [None, int]
    possible: list[bool]  # possible marked by player
    locked: bool

    def __init__(self, x, y, value=None, locked=False):
        self.value = value
        self.possible = [False] * 9
        self.colour = None
        self.locked = locked
        self.x = x
        self.y = y


class sudoku:
    root: Tk
    canvas: Canvas
    chosen: point

    def __init__(self, root):
        self.root = root
        self.canvas = Canvas(self.root)
        self.canvas.pack(fill=BOTH, expand=1)

        self.root.bind("<Key>", self.key)
        self.canvas.bind("<Button-1>", self.callback)

        self.map = []
        for i in range(0, 9):
            a = []
            self.map.append(a)
            for j in range(0, 9):
                a.append(point(i, j))
        m = generate_sudoku.generate_sudoku()
        for i in range(0, 9):
            for j in range(0, 9):
                if m[i][j] != 0:
                    self.map[i][j].value = m[i][j]
                    self.map[i][j].locked = True
        # qself.map[3][3].locked = True
        self.chosen = None
        self.drawMap()

    def key(self, event):
        print(event.char)
        if self.chosen is None:
            return
        if event.char in valid_val:
            if not self.chosen.locked and self.check_valid(int(event.char), self.chosen.x, self.chosen.y):
                self.chosen.value = int(event.char)
        else:
            self.chosen.value = None
        self.drawMap()

    def check_win(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if self.map[i][j].value is None:
                    return False
        return True

    def check_valid(self, value, x, y):
        for i in range(0, 9):
            if self.map[x][i].value == value and i != y:
                return False
            if self.map[i][y].value == value and i != x:
                return False

        square = (x // 3, y // 3)
        for i in range(0, 3):
            x_check = square[0] * 3 + i
            for j in range(0, 3):
                y_check = square[1] * 3 + j
                if self.map[x_check][y_check].value == value and (
                        x_check != x or y_check != y):
                    return False

        return True

    def check_possible(self, x, y):
        poss = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for i in range(0, 9):
            if self.map[x][i].value in poss:
                poss.remove(self.map[x][i].value)
            if self.map[i][y].value in poss:
                poss.remove(self.map[i][y].value)

        square = (x // 3, y // 3)
        for i in range(0, 3):
            x_check = square[0] * 3 + i
            for j in range(0, 3):
                y_check = square[1] * 3 + j
                if self.map[x_check][y_check].value in poss:
                    poss.remove(self.map[x_check][y_check].value)
        return poss

    def callback(self, event):
        mouse_loc = (event.x, event.y)
        print(mouse_loc)
        # check in square
        scaled = ((mouse_loc[0] - GAP) // SHIFT, (mouse_loc[1] - GAP) // SHIFT)
        try:
            if not self.map[scaled[0]][scaled[1]].locked:
                self.chosen = self.map[scaled[0]][scaled[1]]
            else:
                self.chosen = None
            self.drawMap()
        except IndexError:
            pass

    def drawMap(self):
        self.canvas.delete("all")
        for i in range(0, 10):
            linewith = 1
            if i % 3 == 0:
                linewith = 3
            self.canvas.create_line(GAP + (i * SHIFT),
                                    GAP,
                                    GAP + (i * SHIFT),
                                    GAP + SHIFT * 9, width=linewith)
            self.canvas.create_line(GAP,
                                    GAP + (i * SHIFT),
                                    GAP + SHIFT * 9,
                                    GAP + (i * SHIFT), width=linewith)
        # add colour
        if self.chosen is not None:
            self.canvas.create_rectangle(GAP + (self.chosen.x * SHIFT),
                                         GAP + (self.chosen.y * SHIFT),
                                         GAP + ((self.chosen.x + 1) * SHIFT),
                                         GAP + ((self.chosen.y + 1) * SHIFT),
                                         fill="green")

        for i in range(0, 9):
            for j in range(0, 9):
                if self.map[i][j].locked:
                    self.canvas.create_rectangle(GAP + (i * SHIFT) + 3,
                                                 GAP + (j * SHIFT) + 3,
                                                 GAP + ((i + 1) * SHIFT) - 3,
                                                 GAP + ((j + 1) * SHIFT) - 3,
                                                 fill="grey")
                if self.chosen is not None and self.map[i][j].value == self.chosen.value is not None\
                        and self.map[i][j] != self.chosen:
                    self.canvas.create_rectangle(GAP + (i * SHIFT) + 1,
                                                 GAP + (j * SHIFT) + 1,
                                                 GAP + ((i + 1) * SHIFT) - 1,
                                                 GAP + ((j + 1) * SHIFT) - 1,
                                                 fill="#D3D3D3")
                if self.map[i][j].value is not None:
                    self.canvas.create_text(
                        GAP + (i * SHIFT) + (SHIFT // 2),
                        GAP + (j * SHIFT) + (SHIFT // 2),
                        text=str(self.map[i][j].value), font=("Purisa", 15))

        if self.chosen is None:
            poss = {}
        else:
            poss = self.check_possible(self.chosen.x, self.chosen.y)
        for i in range(0, 9):
            color = "Green"
            if i + 1 not  in poss:
                color = "#D3D3D3"
            self.canvas.create_rectangle(GAP + (i * SHIFT) + 1,
                                         GAP + (10 * SHIFT) + 1,
                                         GAP + ((i + 1) * SHIFT) - 1,
                                         GAP + ((11) * SHIFT) - 1,
                                         fill=color)
            self.canvas.create_text(
                GAP + (i * SHIFT) + (SHIFT // 2),
                GAP + (10 * SHIFT) + (SHIFT // 2),
                text=str(i + 1), font=("Purisa", 15))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()
    while True:
        a = sudoku(root)
        root.mainloop()
