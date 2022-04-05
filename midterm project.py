import tkinter as tk
from random import shuffle
import numpy as np
import tkinter.messagebox


root = tk.Tk()
root.geometry('640x640')

canvas = tk.Canvas(root, width=640, height=640)
canvas.pack()


class Field:
    ACTIVE_COLOR = '#2BAE66'
    PASSIVE_COLOR = '#FCF6F5'

    def __init__(self, n, size, c):
        self.n = n
        self.__size = size

        root.bind('<Key>', self.move)
        self.c = c

        self.__block_size = size / n

        numbers = []

        for i in range(0, n ** 2):
            numbers.append(i)

        shuffle(numbers)

        self.matrix = []

        for i in range(n):
            row = []
            for j in range(n):
                b = numbers.pop()

                if b == 0:
                    self.zero = (i, j)

                row.append(b)
            self.matrix.append(row)

        self.draw()


    def draw(self):
        print('Мен иштеп жатам')
        self.c.delete('all')
        for i in range(self.n):
            for j in range(self.n):
                self.c.create_rectangle(
                    j * self.__block_size,
                    i * self.__block_size,
                    (j + 1) * self.__block_size,
                    (i + 1) * self.__block_size,
                    fill=Field.PASSIVE_COLOR if self.matrix[i][j] == 0 else Field.ACTIVE_COLOR
                )

                self.c.create_text(
                    j * self.__block_size + self.__block_size / 2,
                    i * self.__block_size + self.__block_size / 2,
                    text=self.matrix[i][j] if self.matrix[i][j] != 0 else '',
                    font=f'Helvetica {160//self.n} bold',
                    fill=Field.PASSIVE_COLOR
                )

    def move(self, event):
        key = event.keysym.lower()

        if key not in ('down', 'up', 'right', 'left'):
            return
        i = self.zero[0]
        j = self.zero[1]

        if key == 'down':
            if i == 0:
                return

            self.zero = (i - 1, j)
            self.matrix[i][j], self.matrix[i - 1][j] = self.matrix[i - 1][j], self.matrix[i][j]

        elif key == 'up':
            if i == self.n - 1:
                return

            self.zero = (i + 1, j)
            self.matrix[i][j], self.matrix[i + 1][j] = self.matrix[i + 1][j], self.matrix[i][j]
        elif key == 'right':
            if j == 0:
                return

            self.zero = (i, j-1)
            self.matrix[i][j], self.matrix[i][j-1] = self.matrix[i][j-1], self.matrix[i][j]
        elif key == 'left':
            if j == self.n - 1:
                return

            self.zero = (i, j + 1)
            self.matrix[i][j], self.matrix[i][j + 1] = self.matrix[i][j + 1], self.matrix[i][j]

        self.draw()
        self.check_for_end()

    def check_for_end(self):
        na = np.array(self.matrix)

        na = na.reshape((1, self.n ** 2)).tolist()[0]

        if na[:-1] == sorted(na[1:]):
            print(na)
            tk.messagebox.showinfo(message='You won')
        # print(na)


n = int(input('Enter number size of the matrix (1 integer): '))

if n not in range(3, 65):
    raise TypeError('Туура эмес маани киргиздиң, чырагым')

f = Field(n, 640, canvas)

for i in f.matrix:
    print(i)
root.mainloop()