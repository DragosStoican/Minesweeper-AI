# hello_psg.py

import PySimpleGUI as sg
import random
import re
import numpy as np


def figure_out_bombs(row, col):
    total_bombs = 0

    di = [-1, -1, -1, 0, 0, 1, 1, 1]
    dj = [-1, 0, 1, -1, 1, -1, 0, 1]

    # If the square is not on the first row
    for i in range(8):
        new_row = row + di[i]
        new_col = col + dj[i]
        if 0 <= new_row < board_size and 0 <= new_col < board_size:
            if bombs[new_row][new_col] == 1:
                total_bombs += 1

    return total_bombs


# Get game info
nr_bombs = 2
board_size = 5
nr_squares = board_size**2

# Generate random values for bomb locations
bombs = [1 for i in range(nr_bombs)] + [0 for i in range(nr_squares - nr_bombs)]
random.shuffle(bombs)
bombs = np.array(bombs)
bombs = bombs.reshape(board_size, board_size)

layout = [[sg.Button(pad=(0, 0), button_color=("black", "grey"), key=f"button{j}{i}") for i in range(5)] for j in range(5)]

# Create the window
window = sg.Window("Demo", layout)

while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break

    if event == re.compile("button.*").match(event).group():
        print(event)
        square_nr = re.findall("\d+", event)[0]
        row, col = (int(square_nr[0]), int(square_nr[1]))
        print(row, col)

        if bombs[row][col] == 1:
            asset = "bomb_22x22.png"
        else:
            neighbour_bombs = figure_out_bombs(row, col)
            if neighbour_bombs > 0:
                asset = f"minesweeper_{neighbour_bombs}_22x22.png"
            else:
                asset = ""

        window.FindElement(event).Update(button_color=('black', 'white'), image_filename=asset if asset != "" else None,
                                         image_size=(22, 22))
window.close()

