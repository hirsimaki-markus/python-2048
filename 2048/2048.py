"""2048 clone for windows command line"""


import os
import random
from time import sleep
from msvcrt import getch, kbhit


def clear_screen():
    """clear command line"""
    os.system("cls")


def get_control():
    """return next keypress immediately"""
    return chr(ord(getch()))


def init_game(board = [[0, 0, 0, 0] for i in range(4)], score=0):
    """return initial board and score. custom values can be set. board
    should always be a two dimensional list with width and height of 4
    items
    """
    return board, score


def place_tile(board):
    """return board with new tile in previously empty location. tile can
    be 2 (80 % chance) or 4 (20% chance)
    """

    empty_tiles = []

    for i_row, row in enumerate(board): # store empty tiles (zero tiles)
        for i_tile, tile in enumerate(row):
            if tile == 0:
                empty_tiles.append([i_row, i_tile])

    choice = random.choice(empty_tiles)

    board[choice[0]][choice[1]] = random.choice([2, 2, 2, 2, 4])


def print_board(board, score, highscore):
    """prints board, score, highscore and controls"""

    clear_screen()
    number2tile = {0: "       ", # tile formatting dictionary
                   2: "   2   ",
                   4: "   4   ",
                   8: "   8   ",
                  16: "  1 6  ",
                  32: "  3 2  ",
                  64: "  6 4  ",
                 128: "  128  ",
                 256: "  256  ",
                 512: "  512  ",
                1024: "1 0 2 4",
                2048: "2 0 4 8",
                4096: "4 0 9 6",
                8192: "8 1 9 2",
               16384: " 16384 ",
               32768: " 32768 ",
               65536: " 65536 ",
              131072: "131 072"}

    formatting_list = [] # list to use in formatting of the board
    for row in board:
        for number in row: # get tiles with dictionary and add to list
            try:
                formatting_list.append(number2tile[number])
            except KeyError:
                formatting_list.append("SPECIAL") # nonstandard tile
    print("\n    SCORE: {}{} CONTROLS: WASD"
         .format(score, " "*(11-len(str(score)))))
    print("    HIGHSCORE: {}{} QUIT: Q"
         .format(highscore, " "*(14-len(str(highscore)))))
    print("""
    +-------+-------+-------+-------+
    |       |       |       |       |
    |{0}|{1}|{2}|{3}|
    |       |       |       |       |
    +-------+-------+-------+-------+
    |       |       |       |       |
    |{4}|{5}|{6}|{7}|
    |       |       |       |       |
    +-------+-------+-------+-------+
    |       |       |       |       |
    |{8}|{9}|{10}|{11}|
    |       |       |       |       |
    +-------+-------+-------+-------+
    |       |       |       |       |
    |{12}|{13}|{14}|{15}|
    |       |       |       |       |
    +-------+-------+-------+-------+
    """.format(*formatting_list)) # * denotes unpacking


def collapse_board_left(board):
    """collapses board towards left side (zeros act as empty tiles)

    before:     after:

    0 0 0 2     2 0 0 0
    0 2 0 2     2 2 0 0
    4 0 0 2     4 2 0 0
    2 0 0 4     2 4 0 0
    """

    for row_index, row in enumerate(board):
        row = [number for number in row if not number == 0] # strip 0s
        for i in range(4-len(row)): # pad numbers to left with zeroes
            row.append(0)
        board[row_index] = row # save copy board to original board


def combine_tiles_left(board, score):
    """join tiles of the same kind towards left edge. returns new score.
    collapse_board_left should be called before and after this function

    before:     after:

    2 2 0 0    4 0 0 0
    2 2 2 0    4 0 2 0
    4 2 0 0    4 2 0 0
    2 4 0 0    2 4 0 0
    """

    for (row_index, row) in enumerate(board):
        if row[0] == row[1]:
            board[row_index][0] = row[0]+row[1]
            board[row_index][1] = 0
            score += board[row_index][0]
        if row[1] == row[2]:
            board[row_index][1] = row[1]+row[2]
            board[row_index][2] = 0
            score += board[row_index][1]
        if row[2] == row[3]:
            board[row_index][2] = row[2]+row[3]
            board[row_index][3] = 0
            score += board[row_index][2]
    return score


def transpose(matrix):
    """transpose square matrix (two dimensional list)"""
    for index, row in enumerate(list(zip(*matrix))): matrix[index] = list(row)


def reverse_rows(matrix):
    """reverse rows of a matrix"""
    for row in matrix: row.reverse()


def rotate_matrix(matrix, degrees):
    """rotate square matrix. options: 90, -90, 180, -180, 270, -270"""
    # note!!! counter clockwise is positive direction
    degrees = int(degrees)
    if degrees == 90 or degrees == -270:
        reverse_rows(matrix)
        transpose(matrix)
    elif degrees == -90 or degrees == 270:
        transpose(matrix)
        reverse_rows(matrix)
    elif degrees == 180 or degrees == -180:
        reverse_rows(matrix)
        transpose(matrix)
        reverse_rows(matrix)
        transpose(matrix)
    else:
        raise ValueError("Invalid degree of rotation")


def play_move(board, score, highscore):
    """play one turn when user enters valid control. debug mode can be
    accessed with "x" and entering "debug"
    """

    board_copy = [row[:] for row in board] # copy of board

    while True:
        # board is rotated before and after performing move so same
        # functions (collapse_board_left and combine_tiles_left) can be
        # re-used for all directions
        direction = get_control().lower()

        if direction == "w":
            rotate_matrix(board, 90)
            collapse_board_left(board)
            score = combine_tiles_left(board, score)
            collapse_board_left(board)
            rotate_matrix(board, -90)
            if board_copy == board: # check if move did anything or not
                continue
            else:
                break
        elif direction == "a":
            collapse_board_left(board)
            score = combine_tiles_left(board, score)
            collapse_board_left(board)
            if board_copy == board: # check if move did anything or not
                continue
            else:
                break
        elif direction == "s":
            rotate_matrix(board, -90)
            collapse_board_left(board)
            score = combine_tiles_left(board, score)
            collapse_board_left(board)
            rotate_matrix(board, 90)
            if board_copy == board: # check if move did anything or not
                continue
            else:
                break
        elif direction == "d":
            rotate_matrix(board, 180)
            collapse_board_left(board)
            score = combine_tiles_left(board, score)
            collapse_board_left(board)
            rotate_matrix(board, 180)
            if board_copy == board: # check if move did anything or not
                continue
            else:
                break
        elif direction == "q":
            exit("\n            G A M E   Q U I T") # user quit mid-game
        elif direction == "x": # special menu
            code = input("\n    Enter code: ")
            if code == "debug":
                score = _debug(board, score, highscore) # debug mode
            else:
                clear_screen()
                print_board(board, score, highscore)
                continue
        else:
            continue
    return score

def _debug(board, score, highscore):
    """debug mode to be used inside of play_move function. can be used
    to do simple edits on board or score
    """

    clear_screen()
    print_board(board, score, highscore)
    print("\n    Edit board by pressing b or set score by pressing s.")
    control = get_control().lower()
    if control == "b":
        clear_screen()
        print_board(board, score, highscore)
        while True:
            print("""
    guide and example result:

      0 1 2 3 x
    0 · · · ·
    1 · · · ·
    2 · 8 · ·
    3 · · · ·
    y""")
            try:
                x, y, value = input("\n    coordinates and "
                                    "new value (eg: 1 2 8): ").split()
                x = int(x)
                y = int(y)
                value = int(value)
                board[y][x] = value
                clear_screen()
                print_board(board, score, highscore)
                return score
            except Exception:
                clear_screen()
                print_board(board, score, highscore)
                print ("\n    One or more invalid value!")
                continue

        return score
    elif control == "s":
        clear_screen()
        print_board(board, score, highscore)
        while True:
            try:
                score = int(input("\n    set score: "))
                clear_screen()
                print_board(board, score, highscore)
                break
            except ValueError:
                clear_screen()
                print_board(board, score, highscore)
                print ("\n    Invalid value!")
                continue
        return score
    else:
        clear_screen()
        print_board(board, score, highscore)
        return score


def game_over_check(board, score):
    """returns true if game is over. chekcs if any legal moves left"""

    board_copy = [row[:] for row in board] # copy of board

    rotate_matrix(board_copy, 90) # play all possible moves on copy
    collapse_board_left(board_copy)
    score_copy = combine_tiles_left(board_copy, score)
    collapse_board_left(board_copy)
    rotate_matrix(board_copy, -90)

    collapse_board_left(board_copy)
    score_copy = combine_tiles_left(board_copy, score)
    collapse_board_left(board_copy)

    rotate_matrix(board_copy, -90)
    collapse_board_left(board_copy)
    score_copy = combine_tiles_left(board_copy, score)
    collapse_board_left(board_copy)
    rotate_matrix(board_copy, 90)

    rotate_matrix(board_copy, 180)
    collapse_board_left(board_copy)
    score_copy = combine_tiles_left(board_copy, score)
    collapse_board_left(board_copy)
    rotate_matrix(board_copy, 180)

    if board_copy == board: # if true then no moves can be made
        return True
    else:
        return False


def main_game_loop(highscore):
    """main game loop after intro screen and before game over"""
    _ = getch() # catch keyboard hit so its not passed to main game
    board, score = init_game()

    while True:
        place_tile(board)
        print_board(board, score, highscore)
        if game_over_check(board, score) == True:
            break
        print_board(board, score, highscore)
        score = play_move(board, score, highscore)
    return score


def play_intro():
    """Plays intro and continues with keypress"""

    logo_text = ("""
    +-------------------------------+
    |                               |
    |                               |
                               ____
                              6MMMMb
                             6M'  `Mb
      ____     ___           MM    M9
     6MMMMb   6MMMb       ,I YM.  ,9
    MM'  `Mb 6M' `Mb     ,dK  YMMMMb
         ,MM MM   MM    ,dMÄ  6'  `Mb
        ,MM' MM   MM   ,d'MM 6M    MM
      ,M'    MM   MM  ,d' MI MM    MM
    ,M'      YM.  M9 ,d'  MS YM.  ,M9
    MMMMMMMM  YMMM9` MMMMMMRM YMMMM9
                          MI
                          MH
    |                     MM        |
    |                               |
    +-------------------------------+""")

    logo = [
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "_", "_", "_", "_", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "6", "M", "M", "M", "M", "b", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "6", "M", "'", " ", " ", "`", "M", "b"],
    [" ", " ", "_", "_", "_", "_", " ", " ", " ", " ", " ", "_", "_", "_", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "M", "M", " ", " ", " ", " ", "M", "9"],
    [" ", "6", "M", "M", "M", "M", "b", " ", " ", " ", "6", "M", "M", "M", "b", " ", " ", " ", " ", " ", " ", " ", ",", "I", " ", "Y", "M", ".", " ", " ", ",", "9", " "],
    ["M", "M", "'", " ", " ", "`", "M", "b", " ", "6", "M", "'", " ", "`", "M", "b", " ", " ", " ", " ", " ", ",", "d", "K", " ", " ", "Y", "M", "M", "M", "M", "b", " "],
    [" ", " ", " ", " ", " ", ",", "M", "M", " ", "M", "M", " ", " ", " ", "M", "M", " ", " ", " ", " ", ",", "d", "M", "Ä", " ", " ", "6", "'", " ", " ", "`", "M", "b"],
    [" ", " ", " ", " ", ",", "M", "M", "'", " ", "M", "M", " ", " ", " ", "M", "M", " ", " ", " ", ",", "d", "'", "M", "M", " ", "6", "M", " ", " ", " ", " ", "M", "M"],
    [" ", " ", ",", "M", "'", " ", " ", " ", " ", "M", "M", " ", " ", " ", "M", "M", " ", " ", ",", "d", "'", " ", "M", "I", " ", "M", "M", " ", " ", " ", " ", "M", "M"],
    [",", "M", "'", " ", " ", " ", " ", " ", " ", "Y", "M", ".", " ", ",", "M", "9", " ", ",", "d", "'", " ", " ", "M", "S", " ", "Y", "M", ".", " ", " ", ",", "M", "9"],
    ["M", "M", "M", "M", "M", "M", "M", "M", " ", " ", "Y", "M", "M", "M", "9", "`", " ", "M", "M", "M", "M", "M", "M", "R", "M", " ", "Y", "M", "M", "M", "M", "9", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "M", "I", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "M", "H", " ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "M", "M", " ", " ", " ", " ", " ", " ", " ", " ", " "]]

    logo_new = [[" " for x in range(33)] for y in range(14)]

    coordinates = []

    for index_y, row in enumerate(logo):
        for index_x, item in enumerate(row):
            if not item == " ":
                coordinates.append((index_y,index_x))

    random.shuffle(coordinates)

    while coordinates:
        try:
            y, x = coordinates.pop()
            logo_new[y][x] = logo[y][x]
            y, x = coordinates.pop()
            logo_new[y][x] = logo[y][x]
            y, x = coordinates.pop()
            logo_new[y][x] = logo[y][x]
            y, x = coordinates.pop()
            logo_new[y][x] = logo[y][x]
            clear_screen()
            print("\n\n\n")
            for row in logo_new:
                print("    "+"".join(row))
            sleep(0.01)
        except IndexError: # this error should happen and be ignored
            pass

    while not kbhit():
        clear_screen()
        print (logo_text)
        print ("\n         PRESS ENTER KEY TO PLAY")
        sleep(0.5)
        clear_screen()
        print (logo_text)
        sleep(0.5)


def highscore_initialize():
    """checks if highscore file exists and is fully accessible. if it
    doesnt exist, it is initialized if possible. returns true/false
    if file is accessible or not
    """
    try: # outter level to catch unknow exceptions
        try:
            file = open ("highscore", "r")
        except FileNotFoundError: # first run ? initialize highscore
            print ("highscore file not found. Initializing highscore file")
            with open ("highscore", "w") as f:
                f.write("highscore 0")
                f.close()
    except Exception as ex:
        print ("Unexpected exception when trying to acces "
               "highscore file or initialize it: "+type(ex).__name__)
        input ("Press enter to continue without highscore")
        return False

    scoreboard = "./highscore"
    if os.access(scoreboard, os.R_OK) and os.access(scoreboard, os.W_OK):
        return True # scoreboard exists, is readable and writable
    else:
        return False


def highscore_validate():
    """returns current highscore. hash check may be implemented later"""
    file = open ("highscore", "r")
    highscore_data = file.read()
    return highscore_data.split()[1]
    # validity check may use hash file
    # file = open ("highscore", "r")
    # highscore_data = file.read()
    # check validity
    # if valid: return highscore
    # else:
        # with open ("highscore", "w") as f:
            # f.write("highscore 0")
            # f.close()
        # return 0


def save_highscore(highscore):
    """saves highscore to file"""
    with open ("highscore", "w") as f:
        f.write("highscore "+ str(highscore))
        f.close()


def main():
    """2048 clone for windows command line"""
    os.system("title 2048")
    os.system("color A")
    highscore_acces_ok = highscore_initialize() # check accessibility
    if highscore_acces_ok == True:
        highscore = highscore_validate()
    else:
        input("\n    Error accessing highscore file. Press enter to "
              "continue without highscore")
        highscore = 0

    sleep(1) # wait brief moment to display possible errors
    play_intro()

    score = main_game_loop(highscore)

    if highscore_acces_ok == True: # only save highscore if acces was ok
        if score > int(highscore):
            save_highscore(score)
    else:
        input("\n    Error accessing highscore file. Press enter to "
        "continue without saving highscore")
    print ("\n            G A M E   O V E R")


if __name__ == '__main__':
    main()