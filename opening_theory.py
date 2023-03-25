import random
from copy import deepcopy
import multiprocessing
import asyncio


blackInventar = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
whiteInventar = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

names = ['D', 'C', 'J', 'S', 'L', 'N', 'T', 'P', 'K']

inventoryBlack = {}
inventoryWhite = {}

for i in range(len(blackInventar)):
    row = {}
    for j in range(len(names)):
        row[names[j]] = blackInventar[i][j]
    inventoryBlack[i] = row

for i in range(len(whiteInventar)):
    row = {}
    for j in range(len(names)):
        row[names[j]] = whiteInventar[i][j]
    inventoryWhite[i] = row

knight_moves = [(3, 1), (3, -1), (-3, 1), (-3, -1), (1, 3), (1, -3), (-1, 3), (-1, -3)]
kamikaza_moves = [(2, 2), (2, -2), (-2, 2), (-2, -2)]


def get_knight_kamikaza_indices(i, j, board, moves):
    indices = []
    for dr, dc in moves:
        r, c = i + dr, j + dc
        if 0 <= r and r <= 11 and 0 <= c and c <= 11:
            if board[r][c] == None:
                indices.append(str(r) + "N" + str(c))
            elif board[r][c][0] != board[i][j][0]:
                indices.append(str(r) + "J" + str(c))
    return indices


def eliminate_illegal_indices(list_of_moves, board):
    list_exit = []
    if not list_of_moves:
        return list_exit
    for move in list_of_moves:
        if "N" in move:
            ch = "N"
        else:
            ch = "J"
        ch2 = ""
        if "R" in move:
            ch2 = "R"
        elif "L" in move:
            ch2 = "L"
        elif "U" in move:
            ch2 = "U"
        elif "D" in move:
            ch2 = "D"
        coordinates = ""
        directionSniper = ""
        if ch2:
            coordinates = move.split(ch2)[0]
            directionSniper = ch2
        else:
            coordinates = move
        if coordinates == "":
            return list_exit
        i, j = coordinates.split(ch)
        if i.isdigit() and j.isdigit() and 0 <= int(i) <= 11 and 0 <= int(j) <= 11:
            if board[int(i)][int(j)]:
                if board[int(i)][int(j)][1] != "C":
                    list_exit.append(i + ch + j)
            else:
                list_exit.append(i + ch + j)
    return list_exit


def get_all_indices_bishop(i, j, board):
    indices = []
    rows, cols = 12, 12
    r, c, d = i - 1, j + 1, j - 1
    road1 = []
    road2 = []
    while r >= 0 and c < cols:  # lower right and left diagonal
        road1.append((r, c))
        r -= 1
        c += 1
    r = i - 1
    while r >= 0 and d >= 0:
        road2.append((r, d))
        r -= 1
        d -= 1
    indices.append(road1)
    indices.append(road2)
    r, c, d = i + 1, j - 1, j + 1
    road1 = []
    road2 = []
    while r < rows and c >= 0:  # upper left and right diagonal
        road1.append((r, c))
        r += 1
        c -= 1
    r = i + 1
    while r < rows and d < cols:
        road2.append((r, d))
        r += 1
        d += 1
    indices.append(road1)
    indices.append(road2)
    return indices


def get_all_indices_topG(i, j, board):
    indices = []
    rows, cols = 12, 12
    road1 = []
    road2 = []
    for c in range(cols):  # left and right
        if c < j:
            road1.append((i, c))
        elif c > j:
            road2.append((i, c))
    indices.append(road1[::-1])
    indices.append(road2)
    road1 = []
    road2 = []
    for r in range(rows):  # up and down
        if r < i:
            road1.append((r, j))
        elif r > i:
            road2.append((r, j))
    indices.append(road1[::-1])
    indices.append(road2)
    r, c, d = i - 1, j + 1, j - 1
    return indices


def get_all_indices_queen(i, j, board):
    indices = []
    rows, cols = 12, 12
    road1 = []
    road2 = []
    for c in range(cols):  # left and right
        if c < j:
            road1.append((i, c))
        elif c > j:
            road2.append((i, c))
    indices.append(road1[::-1])
    indices.append(road2)
    road1 = []
    road2 = []
    for r in range(rows):  # up and down
        if r < i:
            road1.append((r, j))
        elif r > i:
            road2.append((r, j))
    indices.append(road1[::-1])
    indices.append(road2)
    r, c, d = i - 1, j + 1, j - 1
    road1 = []
    road2 = []
    while r >= 0 and c < cols:  # lower right and left diagonal
        road1.append((r, c))
        r -= 1
        c += 1
    r = i - 1
    while r >= 0 and d >= 0:
        road2.append((r, d))
        r -= 1
        d -= 1
    indices.append(road1)
    indices.append(road2)
    r, c, d = i + 1, j - 1, j + 1
    road1 = []
    road2 = []
    while r < rows and c >= 0:  # upper left and right diagonal
        road1.append((r, c))
        r += 1
        c -= 1
    r = i + 1
    while r < rows and d < cols:
        road2.append((r, d))
        r += 1
        d += 1
    indices.append(road1)
    indices.append(road2)
    return indices


def killOtherFigures(i, j, board, boardNumber):
    if 0 <= i and i <= 11 and 0 <= j and j <= 11:
        if board[i][j] != None and board[i][j][1] != "C":
            if board[i][j][0] == "W":
                inventoryWhite[boardNumber][board[i][j][1]] += 1
            if board[i][j][0] == "B":
                inventoryBlack[boardNumber][board[i][j][1]] += 1
            board[i][j] = None


def find_move_for_list_queen(i0, j0, list_of_indexes, board):
    i_prev, j_prev = "", ""
    i_last, j_last = "", ""
    for i, j in list_of_indexes:
        if board[i][j] is None:
            i_last, j_last = i, j
        else:
            if board[i][j][0] == board[i0][j0][0]:
                return ""
            else:
                return f"{i}J{j}"
        i_prev, j_prev = i, j
    if i_last == "":
        return ""
    return f"{i_last}N{j_last}"


def find_move_for_list_bishop_topG(i0, j0, list_of_indexes, board):
    exit_list = []
    for i, j in list_of_indexes:
        if board[i][j] is None:
            exit_list.append(str(i) + "N" + str(j))
        else:
            if board[i][j][0] == board[i0][j0][0]:
                break
            else:
                exit_list.append(str(i) + "J" + str(j))
                break
    return exit_list


def get_sniper_indices(i, j, board):
    color = board[i][j][0]
    # Initialize list of indices
    indices = []
    if 0 <= i and i <= 11 and 0 <= j + 2 and j + 2 <= 11:
        if board[i][j + 1] == None and board[i][j + 2] == None:
            indices.append(str(i) + "N" + str(j + 2))
    if 0 <= i <= 11 and 0 <= j - 2 <= 11:
        if board[i][j - 1] == None and board[i][j - 2] == None:
            indices.append(str(i) + "N" + str(j - 2))
    if 0 <= i + 2 <= 11 and 0 <= j <= 11:
        if board[i + 1][j] == None and board[i + 2][j] == None:
            indices.append(str(i + 2) + "N" + str(j))
    if 0 <= i - 2 <= 11 and 0 <= j <= 11:
        if board[i - 1][j] == None and board[i - 2][j] == None:
            indices.append(str(i - 2) + "N" + str(j))

    if 0 <= i <= 11 and 0 <= j + 2 <= 11:
        if board[i][j + 1] == None and board[i][j + 2] and board[i][j + 2][0] != color:
            indices.append(str(i) + "J" + str(j+2) + "R")
    if 0 <= i <= 11 and 0 <= j - 2 <= 11:
        if board[i][j - 1] == None and board[i][j - 2] and board[i][j - 2][0] != color:
            indices.append(str(i) + "J" + str(j-2) + "L")
    if 0 <= i + 2 <= 11 and 0 <= j <= 11:
        if board[i + 1][j] == None and board[i + 2][j] and board[i + 2][j][0] != color:
            indices.append(str(i+2) + "J" + str(j) + "U")
    if 0 <= i - 2 <= 11 and 0 <= j <= 11:
        if board[i - 1][j] == None and board[i - 2][j] and board[i - 2][j][0] != color:
            indices.append(str(i-2) + "J" + str(j) + "D")

    return indices


def moves(i, j, board):
    listOfMoves = []
    figure = board[i][j]
    if figure == None:
        return []
    color = figure[0]
    figureType = figure[1]
    if figureType == "P":  # Pawn
        if color == "W":
            if j < 11 and i < 11 and board[i + 1][j + 1] == None:
                listOfMoves.append(str(i + 1) + "N" + str(j + 1))  # string as following: i + N/J + j
            if j > 0 and i < 11 and board[i + 1][j - 1] == None:
                listOfMoves.append(str(i + 1) + "N" + str(j - 1))
            if board[i + 1][j] and board[i + 1][j][0] == "B":
                listOfMoves.append(str(i + 1) + "J" + str(j))  # N = doesn't eat    J = eat
            if i == 1 and j < 10 and board[i + 1][j + 1] == None and board[i + 2][j + 2] == None:
                listOfMoves.append(str(i + 2) + "N" + str(j + 2))
            if i == 1 and j > 1 and board[i + 1][j - 1] == None and board[i + 2][j - 2] == None:
                listOfMoves.append(str(i + 2) + "N" + str(j - 2))
        if color == "B":
            if j < 11 and i > 0 and board[i - 1][j + 1] == None:
                listOfMoves.append(str(i - 1) + "N" + str(j + 1))
            if j < 11 and i > 0 and board[i - 1][j - 1] == None:
                listOfMoves.append(str(i - 1) + "N" + str(j - 1))
            if board[i - 1][j] and board[i - 1][j][0] == "W":
                listOfMoves.append(str(i - 1) + "J" + str(j))
            if i == 10 and j < 10 and board[i - 1][j + 1] == None and board[i - 2][j + 2] == None:
                listOfMoves.append(str(i - 2) + "N" + str(j + 2))
            if i == 10 and j > 1 and board[i - 1][j - 1] == None and board[i - 2][j - 2] == None:
                listOfMoves.append(str(i - 2) + "N" + str(j - 2))

        return eliminate_illegal_indices(listOfMoves, board)
    elif figureType == "K":  # King
        for x in [i - 1, i, i + 1]:
            for y in [j - 1, j, j + 1]:
                if 0 <= x <= 11 and 0 <= y <= 11:
                    if board[x][y] == None and not (x == i and y == i):
                        listOfMoves.append(str(x) + "N" + str(y))
                    if board[x][y] and board[x][y][0] != color and not (x == i and y == i):
                        listOfMoves.append(str(x) + "J" + str(y))
        return eliminate_illegal_indices(listOfMoves, board)
    elif figureType == "D":  # Dama
        listOfRoads = get_all_indices_queen(i, j, board)
        for road in listOfRoads:
            listOfMovesHelp = find_move_for_list_queen(i, j, road, board)
            if isinstance(listOfMovesHelp, list):
                for helper in listOfMovesHelp:
                    listOfMoves.append(helper)
            else:
                listOfMoves.append(listOfMovesHelp)
        return eliminate_illegal_indices(listOfMoves, board)
    elif figureType == "L":  # L = bishop
        listOfRoads = get_all_indices_bishop(i, j, board)
        for road in listOfRoads:
            listOfMovesHelp = find_move_for_list_bishop_topG(i, j, road, board)
            if isinstance(listOfMovesHelp, list):
                for helper in listOfMovesHelp:
                    listOfMoves.append(helper)
            else:
                listOfMoves.append(listOfMovesHelp)
        return eliminate_illegal_indices(listOfMoves, board)
    elif figureType == "N":  # N = knight
        listOfMoves = get_knight_kamikaza_indices(i, j, board, knight_moves)
        return eliminate_illegal_indices(listOfMoves, board)
    elif figureType == "T":  # T = rook
        listOfRoads = get_all_indices_topG(i, j, board)
        for road in listOfRoads:
            listOfMovesHelp = find_move_for_list_bishop_topG(i, j, road, board)
            if isinstance(listOfMovesHelp, list):
                for helper in listOfMovesHelp:
                    listOfMoves.append(helper)
            else:
                listOfMoves.append(listOfMovesHelp)
        return eliminate_illegal_indices(listOfMoves, board)
    elif figureType == "C":  # Brick
        for x in [i - 1, i, i + 1]:
            for y in [j - 1, j, j + 1]:
                if 0 <= x <= 11 and 0 <= y <= 11:
                    if board[x][y] == None and not (x == i and y == i):
                        listOfMoves.append(str(x) + "N" + str(y))
        return eliminate_illegal_indices(listOfMoves, board)
    elif figureType == "S":  # sniper
        listOfMoves = get_sniper_indices(i, j, board)
        return eliminate_illegal_indices(listOfMoves, board)
    elif figureType == "J":  # kamikaza
        # RIP
        listOfMoves = get_knight_kamikaza_indices(i, j, board, kamikaza_moves)
        return eliminate_illegal_indices(listOfMoves, board)
    return


def make_a_move(i, j, board, nextMove, boardNumber):
    not_boardNumber = int(not boardNumber)
    figure = board[i][j]
    if figure != None:
        color = figure[0]
        figureType = figure[1]
        if "N" in nextMove:
            ch = "N"
        else:
            ch = "J"
        ch2 = ""
        if "R" in nextMove:
            ch2 = "R"
        elif "L" in nextMove:
            ch2 = "L"
        elif "U" in nextMove:
            ch2 = "U"
        elif "D" in nextMove:
            ch2 = "D"
        coordinates = ""
        directionSniper = ""
        if ch2:
            coordinates, directionSniper = nextMove.split(ch2)
        else:
            coordinates = nextMove
        next_i, next_j = coordinates.split(ch)
        next_i = int(next_i)
        next_j = int(next_j)
        if board[next_i][next_j] != None:
            moves_kamikaza = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            killedFigure = board[next_i][next_j]
            if killedFigure[0] == "W":
                inventoryWhite[int(boardNumber)][killedFigure[1]] += 1
            if killedFigure[0] == "B":
                inventoryBlack[int(boardNumber)][killedFigure[1]] += 1
            if figureType == "J":
                moves_kamikaza = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                for dr, dc in moves_kamikaza:
                    r, c = next_i + dr, next_j + dc
                    killOtherFigures(r, c, board, not_boardNumber)
            if figureType == "T":
                if board[next_i][next_j] != None:
                    killedFigure = board[next_i][next_j]
                    if killedFigure[0] == "W":
                        inventoryWhite[int(boardNumber)][killedFigure[1]] += 1
                    if killedFigure[0] == "B":
                        inventoryBlack[int(boardNumber)][killedFigure[1]] += 1
                    if i == next_i:
                        if next_j < j:
                            killOtherFigures(i, next_j - 1, board, int(boardNumber))
                        if next_j > j:
                            killOtherFigures(i, next_j + 1, board, int(boardNumber))
                    if j == next_j:
                        if next_i < i:
                            killOtherFigures(next_i - 1, j, board, int(boardNumber))
                        if next_i > i:
                            killOtherFigures(next_i + 1, j, board, int(boardNumber))
            killedFigure = board[next_i][next_j]
            if killedFigure[1] == "L":
                around_bishop = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                for dr, dc in moves_kamikaza:
                    r, c = next_i + dr, next_j + dc
                    killOtherFigures(r, c, board, not_boardNumber)
        if next_i == i and next_j == j and board[i][j][1] == "S":
            killedFigure = ""
            if directionSniper == "R":
                killedFigure = board[i][j + 1]
            elif directionSniper == "L":
                killedFigure = board[i][j - 1]
            elif directionSniper == "U":
                killedFigure = board[i + 1][j]
            elif directionSniper == "D":
                killedFigure = board[i - 1][j]
            if board[i][j][0] == "W":
                inventoryWhite[int(boardNumber)][killedFigure[1]] += 1
            if board[i][j][0] == "B":
                inventoryBlack[int(boardNumber)][killedFigure[1]] += 1
        board[i][j] = None
        if figureType != "J" or (figureType == "J" and ch == "N"):
            board[next_i][next_j] = figure
        else:
            board[next_i][next_j] = None


def isLegalForPut(board, figure, i, j, boardNumber):  # only call if inventory is not empty
    color = figure[0]
    figureType = figure[1]
    if color == "W":
        if inventoryWhite[int(boardNumber)][figureType] <= 0:
            return 0
    if color == "B":
        if inventoryBlack[int(boardNumber)][figureType] <= 0:
            return 0
    if figureType == "P":
        if i < 1 or i > 10:
            return 0
    if board[i][j] == None:
        return 1
    return 0


def putFigure(board, figure, i, j, boardNumber):
    color = figure[0]
    figureType = figure[1]
    board[i][j] = figure
    if color == "W":
        inventoryWhite[int(boardNumber)][figureType] -= 1
    if color == "B":
        inventoryBlack[int(boardNumber)][figureType] -= 1


def simulate_random_turn(board, color, boardNumber):
    if color == "W":
        values = list(inventoryWhite[boardNumber].values())
        total = sum(values)
        result = random.randint(0, 1)
        if result and total > 0:
            valid_keys = [key for key, value in inventoryWhite[boardNumber].items() if value > 0]
            random_key = random.choice(valid_keys)
            valid_position = 0
            while not valid_position:
                i = random.randint(0, 11)
                j = random.randint(0, 11)
                result = isLegalForPut(board, str("W") + random_key, i, j, boardNumber)
                if result == 1:
                    valid_position = True
            putFigure(board, str("W") + random_key, i, j, boardNumber)
        else:
            color_position = None
            while color_position is None:
                # Generate random values for i and j
                i = random.randint(0, 11)
                j = random.randint(0, 11)
                # Check if the piece at (i, j) is white
                mlist = moves(i, j, board)
                if board[i][j] != None:
                    if board[i][j][0] == color and len(mlist) != 0:
                        color_position = (i, j)
                        make_a_move(i, j, board, random.choice(mlist), boardNumber)
    if color == "B":
        values = list(inventoryBlack[boardNumber].values())
        total = sum(values)
        result = random.randint(0, 1)
        if result and total > 0:
            valid_keys = [key for key, value in inventoryBlack[boardNumber].items() if value > 0]
            random_key = random.choice(valid_keys)
            valid_position = 0
            while not valid_position:
                i = random.randint(0, 11)
                j = random.randint(0, 11)
                result = isLegalForPut(board, str("B") + random_key, i, j, boardNumber)
                if result == 1:
                    valid_position = True
            putFigure(board, str("B") + random_key, i, j, boardNumber)
        else:
            color_position = None
            while color_position is None:
                i = random.randint(0, 11)
                j = random.randint(0, 11)
                mlist = moves(i, j, board)
                if board[i][j] != None:
                    if board[i][j][0] == color and len(mlist) != 0:
                        color_position = (i, j)
                        make_a_move(i, j, board, random.choice(mlist), boardNumber)


board1 = [[None, None, None, None, None, None, None, None, None, None, None, None],
         ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
         [None, None, None, None, None, None, None, None, None, None, None, None]]

board = [['WT', 'WN', 'WL', 'WD', 'WK', 'WL', 'WN', 'WT', 'WJ', 'WS', 'WC', 'WD'],
         ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP'],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None, None, None, None],
         ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP'],
         ['BT', 'BN', 'BL', 'BD', 'BK', 'BL', 'BN', 'BT', 'BJ', 'BS', 'BC', 'BD']]


def score(board, color):
    sumVariable = 0
    for i in range(12):
        for j in range(12):
            if board[i][j] != None:
                if board[i][j][0] == color:
                    if board[i][j][1] == "P":
                        sumVariable += 1
                    elif board[i][j][1] == "N":
                        sumVariable += 4
                    elif board[i][j][1] == "L":
                        sumVariable += 2
                    elif board[i][j][1] == "T":
                        sumVariable += 6
                    elif board[i][j][1] == "S":
                        sumVariable += 2.5
                    elif board[i][j][1] == "J":
                        sumVariable += 6
                    elif board[i][j][1] == "D":
                        sumVariable += 7
                    elif board[i][j][1] == "K":
                        sumVariable += 10000
                else:
                    if board[i][j][1] == "P":
                        sumVariable -= 1
                    elif board[i][j][1] == "N":
                        sumVariable -= 4
                    elif board[i][j][1] == "L":
                        sumVariable -= 2
                    elif board[i][j][1] == "T":
                        sumVariable -= 6
                    elif board[i][j][1] == "S":
                        sumVariable -= 2.5
                    elif board[i][j][1] == "J":
                        sumVariable -= 6
                    elif board[i][j][1] == "D":
                        sumVariable -= 7
                    elif board[i][j][1] == "K":
                        sumVariable -= 10000
    return sumVariable


def getScore(board, color, boardNumber):
    scoreValue = -100
    true_i = -1
    true_j = -1
    true_move = ""
    for i in range(12):
        for j in range(12):
            if board[i][j] != None:
                if board[i][j][0] == color:
                    listOfMoves = moves(i, j, board)
                    for move in listOfMoves:
                        bor = deepcopy(board)
                        make_a_move(i, j, bor, move, boardNumber)
                        if score(bor, color) >= scoreValue:
                            scoreValue = score(bor, color)
                            true_i = i
                            true_j = j
                            true_move = move
    # print("scoreValue", scoreValue)
    return true_i, true_j, true_move, scoreValue


def react(board, color, boardNumber):
    scoreValue = -100
    true_i = -1
    true_j = -1
    true_move = ""
    for i in range(12):
        for j in range(12):
            if board[i][j] != None:
                if board[i][j][0] == color:
                    listOfMoves = moves(i, j, board)
                    for move in listOfMoves:
                        bor = deepcopy(board)
                        make_a_move(i, j, bor, move, boardNumber)
                        if color == "W":
                            colour = "B"
                        else:
                            colour = "W"
                        i_hat, j_hat, move_hat, score_hat = getScore(bor, colour, boardNumber)
                        if score_hat >= scoreValue:
                            scoreValue = score_hat
                            true_i = i_hat
                            true_j = j_hat
                            true_move = move_hat
    # print("scoreValue", scoreValue)
    return true_i, true_j, true_move


def visualize_board(board):
    print("    0 -  - 1 -  - 2 - - 3 -  - 4 -  - 5 - - 6 -  - 7 -  - 8 - - 9 -  - 10 -  - 11")
    print("  -----------------------")
    for i in range(12):
        row = " - "
        for j in range(12):
            if board[i][j] is None:
                row += "* "
            else:
                row += board[i][j]
            row += " - "
        print(f"{i} |{row}| {i}")
    print("  -----------------------")
    print("    0 -  - 1 -  - 2 - - 3 -  - 4 -  - 5 - - 6 -  - 7 -  - 8 - - 9 -  - 10 -  - 11")


if __name__ == '__main__':

    visualize_board(board)

    while True:
        i = int(input("i ->"))
        j = int(input("j ->"))
        M = input("Move ->")
        make_a_move(i, j, board, M, True)
        i, j, M, val = getScore(board, "B", True)
        print(i, j, M)
        make_a_move(i, j, board, M, True)
        visualize_board(board)
