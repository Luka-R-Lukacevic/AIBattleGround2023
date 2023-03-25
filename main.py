from markings_parser import *
from server_connection import *
from game_mechanics import *
from copy import deepcopy
from time import sleep
from opening_theory import *

our_name = "gpt3d"


def setup_connection():
    token = get_token("player1", "sifra1")
    if join_game(1, token)['playerOne'] == our_name:
        board_num = False
    else:
        board_num = True
    sleep(2)
    print("Connection successful")

    return token, board_num


def setUpPlayer(token):
    make_move(token, "P-S-11-11")
    sleep(0.1)
    make_move(token, "P-N-0-1")
    sleep(0.1)
    make_move(token, "P-N-11-10")
    sleep(0.1)
    make_move(token, "P-L-0-2")
    sleep(0.1)
    make_move(token, "P-L-11-9")
    sleep(0.1)
    make_move(token, "P-T-0-3")
    sleep(0.1)
    make_move(token, "P-T-11-8")
    sleep(0.1)
    make_move(token, "P-D-0-4")
    sleep(0.1)
    make_move(token, "P-D-11-7")
    sleep(0.1)
    make_move(token, "P-K-0-5")
    sleep(0.1)
    make_move(token, "P-K-11-6")
    sleep(0.1)
    make_move(token, "P-C-0-6")
    sleep(0.1)
    make_move(token, "P-C-11-5")
    sleep(0.1)
    make_move(token, "P-D-0-7")
    sleep(0.1)
    make_move(token, "P-D-11-4")
    sleep(0.1)
    make_move(token, "P-T-0-8")
    sleep(0.1)
    make_move(token, "P-T-11-3")
    sleep(0.1)
    make_move(token, "P-L-0-9")
    sleep(0.1)
    make_move(token, "P-L-11-2")
    sleep(0.1)
    make_move(token, "P-N-0-10")
    sleep(0.1)
    make_move(token, "P-N-11-1")
    sleep(0.1)
    make_move(token, "P-J-0-11")
    sleep(0.1)
    return parse_return(make_move(token, "P-J-11-0"))  # crni


def main():
    state = True
    token, board_num = setup_connection()

    make_move(token, "P-S-0-0")  # bijeli

    sleep(0.1)

    board1, board2 = setUpPlayer(token)

    parsed_boards = {
        0: parse_board(board1),
        1: parse_board(board2)
    }

    k = 1
    while state:

        if k % 2 == 0:
            cha = "W"
        else:
            cha = "B"
        k += 1

        board_num = not board_num

        i, j, move = react(parsed_boards[board_num], cha, board_num)

        print(i, j, move)

        if "J" in move:
            ch = "J"
        else:
            ch = "N"
        i1, j1 = move.split(ch)

        board1, board2 = parse_return(make_move(token, parse_move("M", i, j, i1, j1)))

        parsed_boards = {
            0: parse_board(board1),
            1: parse_board(board2)
        }


if __name__ == '__main__':
    main()
