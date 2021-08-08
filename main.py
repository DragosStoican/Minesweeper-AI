# hello_psg.py

import PySimpleGUI as sg
import random
import re
import numpy as np

# Get game info
nr_bombs = 2
board_size = 5
nr_squares = board_size ** 2

# Generate random values for bomb locations
bombs = [1 for i in range(nr_bombs)] + [0 for i in range(nr_squares - nr_bombs)]
random.shuffle(bombs)
bombs = np.array(bombs)
bombs = bombs.reshape(board_size, board_size)

layout = [[sg.Button(pad=(0, 0), button_color=("black", "grey"), key=f"button{j}{i}") for i in range(5)] for j in
          range(5)]

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


def cascade(row, col):
    di = [-1, -1, -1, 0, 0, 1, 1, 1]
    dj = [-1, 0, 1, -1, 1, -1, 0, 1]

    for i in range(8):
        new_row = row + di[i]
        new_col = col + dj[i]
        if 0 <= new_row < board_size and 0 <= new_col < board_size:
            if bombs[new_row][new_col] != -1:
                tile_click_event(new_row, new_col)


def tile_click_event(row, col):
    if bombs[row][col] == 1:
        asset = "bomb_22x22.png"
    else:
        bombs[row][col] = -1
        neighbour_bombs = figure_out_bombs(row, col)
        if neighbour_bombs > 0:
            asset = f"minesweeper_{neighbour_bombs}_22x22.png"
        else:
            # No neighbour bomb means we have to cascade clear tiles
            asset = ""
            cascade(row, col)

    layout[row][col].Update(button_color=('black', 'white'), image_filename=asset if asset != "" else None,
                            image_size=(22, 22))


def tile_rightclick_event(row, col):
    layout[row][col].Update(button_color=('black', 'white'), image_filename="minesweeper_flag_22x22.png",
                            image_size=(22, 22))








# Create the window
window = sg.Window("Demo", layout, finalize=True)


# for button in np.array(layout).flatten():
#     button.bind('<Button-3>', tile_click_event)
for i in range(5):
    for j in range(5):
        layout[i][j].bind('<Button-3>', f" -rightclicked")





while True:
    event, values = window.read()
    # End program if user closes window
    if event == sg.WIN_CLOSED:
        break

    if event == re.compile("button[0-9]+").match(event).group():
        square_nr = re.findall("\d+", event)[0]
        row, col = (int(square_nr[0]), int(square_nr[1]))

        tile_click_event(row, col)

    elif event == re.compile("button[0-9]+.*-rightclicked").match(event).group():
        square_nr = re.findall("\d+", event)[0]
        row, col = (int(square_nr[0]), int(square_nr[1]))
        tile_rightclick_event(row, col)

window.close()
