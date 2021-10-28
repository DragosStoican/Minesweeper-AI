# hello_psg.py
# Need to use pillow to modify the images before I put them onto buttons!

import PySimpleGUI as sg
import random
import re
import numpy as np
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

# Get game info
board_size = 10
nr_squares = board_size ** 2
nr_bombs = nr_squares // 10

# Asset size info
window_width, window_height = sg.Window.get_screen_size()
window_size = min(window_width, window_height)
window_padding = int(0.05 * window_size)
button_size = int((window_size - window_padding) / board_size)

# Generate random values for bomb locations
bombs = [1 for i in range(nr_bombs)] + [0 for i in range(nr_squares - nr_bombs)]
random.shuffle(bombs)
bombs = np.array(bombs)
bombs = bombs.reshape(board_size, board_size)

# Define button logic
left_mouse_pressed = False
right_mouse_pressed = False


def figure_out_bombs(row, col):
    total_bombs = 0

    di = [-1, -1, -1, 0, 0, 1, 1, 1]
    dj = [-1, 0, 1, -1, 1, -1, 0, 1]

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
        asset = assets['bomb']
    else:
        bombs[row][col] = -1
        neighbour_bombs = figure_out_bombs(row, col)
        if neighbour_bombs > 0:
            asset = assets[f"minesweeper_{neighbour_bombs}"]
        else:
            # No neighbour bomb means we have to cascade clear tiles
            asset = assets['empty']
            cascade(row, col)

    layout[row][col].Widget.config(image=asset, width=button_size, height=button_size)


# def tile_click_event(event, row, col):
#     _tile_click_event(row, col)


def tile_right_click_event(event, row, col):
    layout[row][col].Widget.config(image=assets['minesweeper_flag'], width=button_size, height=button_size)


def create_assets():
    output = dict()
    asset_list = ["bomb", "minesweeper_1", "minesweeper_2", "minesweeper_3", "minesweeper_4", "minesweeper_5",
                  "minesweeper_6", "minesweeper_7", "minesweeper_8", "minesweeper_flag", "unclicked", "empty"]
    for asset in asset_list:
        orig_img = Image.open(f"assets/{asset}.png")
        orig_img = orig_img.resize((button_size, button_size), Image.ANTIALIAS)

        output[f"{asset}"] = ImageTk.PhotoImage(orig_img)

    return output


def clear_around_tile(row, col):
    di = [-1, -1, -1, 0, 0, 1, 1, 1]
    dj = [-1, 0, 1, -1, 1, -1, 0, 1]

    for i in range(8):
        new_row = row + di[i]
        new_col = col + dj[i]
        if 0 <= new_row < board_size and 0 <= new_col < board_size:
            if layout[new_row][new_col].Widget.cget('image') != str(assets['minesweeper_flag']):
                tile_click_event(new_row, new_col)


def anyButtonPressed(event, row, col):
    global left_mouse_pressed
    global right_mouse_pressed
    if event.num == 1:
        left_mouse_pressed = True
    if event.num == 3:
        right_mouse_pressed = True
    if left_mouse_pressed and right_mouse_pressed:
        clear_around_tile(row, col)
    elif event.num == 1:
        tile_click_event(row, col)
    elif event.num == 3:
        tile_right_click_event(event, row, col)


def reset_pressed_state(event):
    global left_mouse_pressed
    global right_mouse_pressed
    left_mouse_pressed = False
    right_mouse_pressed = False


if __name__ == "__main__":
    # Define buttons
    layout = [[sg.Button(pad=(0, 0), key=f"button{j}{i}") for i in range(board_size)] for j in
              range(board_size)]

    # Create the window
    window = sg.Window("Demo", layout, size=(window_width, window_height), finalize=True)
    window.Maximize()

    # Get the assets modified by pillow
    assets = create_assets()
    # print(str(assets['minesweeper_flag']))
    # Assign appropiate assets to buttons
    for list in layout:
        for button in list:
            button.Widget.config(image=assets['unclicked'], width=button_size, height=button_size)

    for i in range(board_size):
        for j in range(board_size):
            layout[i][j].Widget.bind('<Button-1>', lambda event, row=i, col=j: anyButtonPressed(event, row, col))
            layout[i][j].Widget.bind('<Button-3>', lambda event, row=i, col=j: anyButtonPressed(event, row, col))
            layout[i][j].Widget.bind('<ButtonRelease-1>', reset_pressed_state)
            layout[i][j].Widget.bind('<ButtonRelease-3>', reset_pressed_state)

    while True:
        event, values = window.read()
        # End program if user closes window
        if event == sg.WIN_CLOSED:
            break

    window.close()
