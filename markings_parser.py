import json


'''OUR_MARKINGS = {
    "P": "P",   # Pijan
    "Q": "K",   # Kralj
    "C": "C",   # Cigla
    "N": "D",   # Dama
    "K": "J",   # Kamikaza
    "L": "N",   # Ludi konj
    "D": "L",   # Drop a live grenade lovac
    "T": "T",   # TopG
    "S": "S",   # Snajper ubio
}

THEIR_MARKINGS = {v: k for k, v in OUR_MARKINGS.items()}'''


def parse_return(_return):  # board number can be 1 or 2
    board_string = "boardState"

    return json.loads(_return['gameState'])[board_string + "1"]["board"], json.loads(_return['gameState'])[board_string + "2"]["board"]


def parse_board(board):
    # cnt = 0
    return_list = []
    temp_list = []

    for i, _list in enumerate(board):
        for j, _figure in enumerate(_list):
            parsed = parse_figure(_figure)
            # print("Parsed figure:", parsed)
            temp_list.append(parsed)
            # cnt += 1
        return_list.append(temp_list)
        temp_list = []

    # print(f"Number of elements is {cnt}")
    return return_list


def parse_figure(figure):
    if figure is None:
        return None

    s = ""

    if not figure["black"]:
        s += "W"
    else:
        s += "B"

    return s + figure["oznaka"]


def parse_move(_type, row, column, row_to=None, column_to=None):
    if _type == "P":
        return "P" + "-" + str(row) + "-" + str(column)
    else:
        return "M" + "-" + str(row) + "-" + str(column) + "-" + str(row_to) + "-" + str(column_to)


def parse_board_test():
    _return = [
        [{'id': 0, 'oznaka': 'K', 'black': False}, None, None, None, None, None, None, None, None, None, None, None],
        [{'id': 0, 'oznaka': 'P', 'black': False}, {'id': 1, 'oznaka': 'P', 'black': False},
         {'id': 2, 'oznaka': 'P', 'black': False}, {'id': 3, 'oznaka': 'P', 'black': False},
         {'id': 4, 'oznaka': 'P', 'black': False}, {'id': 5, 'oznaka': 'P', 'black': False},
         {'id': 6, 'oznaka': 'P', 'black': False}, {'id': 7, 'oznaka': 'P', 'black': False},
         {'id': 8, 'oznaka': 'P', 'black': False}, {'id': 9, 'oznaka': 'P', 'black': False},
         {'id': 10, 'oznaka': 'P', 'black': False}, {'id': 11, 'oznaka': 'P', 'black': False}],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None, None, None],
        [{'id': 12, 'oznaka': 'P', 'black': True}, {'id': 13, 'oznaka': 'P', 'black': True},
         {'id': 14, 'oznaka': 'P', 'black': True}, {'id': 15, 'oznaka': 'P', 'black': True},
         {'id': 16, 'oznaka': 'P', 'black': True}, {'id': 17, 'oznaka': 'P', 'black': True},
         {'id': 18, 'oznaka': 'P', 'black': True}, {'id': 19, 'oznaka': 'P', 'black': True},
         {'id': 20, 'oznaka': 'P', 'black': True}, {'id': 21, 'oznaka': 'P', 'black': True},
         {'id': 22, 'oznaka': 'P', 'black': True}, {'id': 23, 'oznaka': 'P', 'black': True}],
        [None, None, None, None, None, None, None, None, None, None, None, None]]

    parse_board(_return)


def parse_move_test():
    print(parse_move("P", "WK", 3, 2))
    print(parse_move("M", "BL", 3, 2, 5, 6))


if __name__ == '__main__':
    parse_board_test()
    parse_move_test()
