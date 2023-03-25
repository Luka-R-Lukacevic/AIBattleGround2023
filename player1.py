from server_connection import *
from markings_parser import *
from time import sleep


if __name__ == '__main__':
    player1_token = get_token("player1", "sifra1")

    print(json.loads(join_game(1, player1_token)['gameState'])["boardState1"]['board'])
    sleep(2)

    board1, board2 = parse_return(make_move(player1_token, "P-K-0-3"))
    parsed_board1 = parse_board(board1)
    parsed_board2 = parse_board(board2)
    print(parsed_board1, parsed_board2)
