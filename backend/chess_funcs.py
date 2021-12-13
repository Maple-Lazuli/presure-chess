from scipy import stats
import numpy as np
import chess
import tensorflow as tf

pieces = {
    '0': {
        'name': 'Space'
    },
    '1': {
        'name': 'Rook',
        'base': -1,
        'value': 5
    },
    '2': {
        'name': 'Knight',
        'base': -1,
        'value': 3
    },
    '3': {
        'name': 'Bishop',
        'base': -1,
        'value': 3
    },
    '4': {
        'name': 'Queen',
        'base': -1,
        'value': 9
    },
    '5': {
        'name': 'King',
        'base': -1,
        'value': 10
    },
    '6': {
        'name': 'Bishop',
        'base': -1,
        'value': 3
    },
    '9': {
        'name': 'BPawn',
        'base': -1,
        'value': 1
    },
    '11': {
        'name': 'Rook',
        'base': 1,
        'value': 5
    },
    '12': {
        'name': 'Knight',
        'base': 1,
        'value': 3
    },
    '13': {
        'name': 'Bishop',
        'base': 1,
        'value': 3
    },
    '14': {
        'name': 'Queen',
        'base': 1,
        'value': 9
    },
    '15': {
        'name': 'King',
        'base': 1,
        'value': 10
    },
    '16': {
        'name': 'Bishop',
        'base': 1,
        'value': 3
    },
    '10': {
        'name': 'WPawn',
        'base': 1,
        'value': 1
    },
}


# Create Helper Functions for visualizations

def print_matrix(arr):
    """
    Prints out the chess matrix into an text representation.
    :param arr: The chess positions as a 1x64 matrix
    :return: None
    """
    string = ""
    for i in range(1, 65):
        string += translation(arr[i - 1]) + ' '
        if i % 8 == 0:
            print(string)
            string = ""


def translation(int_val):
    """
    Translates the numeric representation on of the chess board to a character based
    representation of the board. Lower case characters are used for Black while upper
    case characters are used for white
    :param int_val: The integer value representing a chess piece
    :return: A character representing a chess piece
    """
    int_val = int(int_val)
    if int_val == 0:
        return '_'
    elif int_val == 1:
        return 'r'
    elif int_val == 2:
        return 'n'
    elif int_val == 3:
        return 'b'
    elif int_val == 4:
        return 'q'
    elif int_val == 5:
        return 'k'
    elif int_val == 6:
        return 'b'
    elif int_val == 9:
        return 'p'
    elif int_val == 10:
        return 'P'
    elif int_val == 11:
        return 'R'
    elif int_val == 12:
        return 'N'
    elif int_val == 13:
        return 'B'
    elif int_val == 14:
        return 'Q'
    elif int_val == 15:
        return 'K'
    elif int_val == 16:
        return 'B'


def rook(index, weight=1.0, current_board=np.zeros((8, 8), dtype=np.float)):
    """
    Calculates the area of effect and weight of effect for a Rook at a particular
    index on the board.
    :param index: The position of the piece on the board
    :param weight: The weight the piece can put on the board
    :param current_board: The current chess board as a 8x8 matrix. This is used to calculate piece limits
    :return: 8x8 Matrix with piece weights.
    """
    baseline = np.zeros((8, 8), dtype=np.float)
    y = index[0]
    x = index[1]
    # left row
    for i in range(x - 1, -1, -1):
        baseline[y, i] = weight
        if current_board[y, i] != 0:
            break
    # right row
    for i in range(x + 1, 8):
        baseline[y, i] = weight
        if current_board[y, i] != 0:
            break
    # top column
    for i in range(y - 1, -1, -1):
        baseline[i, x] = weight
        if current_board[i, x] != 0:
            break
    # bottom column
    for i in range(y + 1, 8):
        baseline[i, x] = weight
        if current_board[i, x] != 0:
            break
    baseline[y, x] = 0
    return baseline


def bishop(index, weight=1.0, current_board=np.zeros((8, 8), dtype=np.float)):
    """
    Calculates the area of effect and weight of effect for a Bishop at a particular
    index on the board.
    :param index: The position of the piece on the board
    :param weight: The weight the piece can put on the board
    :param current_board: The current chess board as a 8x8 matrix. This is used to calculate piece limits
    :return: 8x8 Matrix with piece weights.
    """
    baseline = np.zeros((8, 8), dtype=np.float)
    y = index[0]
    x = index[1]
    # upper left
    for i in range(0, 8):
        try:
            x1 = x - i
            y1 = y - i
            if (x1 == x) and (y1 == y):
                continue
            if (x1 >= 0) and (y1 >= 0):
                baseline[y1, x1] = weight
                # print(baseline)
                if current_board[y1, x1] != 0:
                    break
        except IndexError:
            pass
    # lower left
    for i in range(0, 8):
        try:
            x1 = x - i
            y1 = y + i
            if (x1 == x) and (y1 == y):
                continue
            if (x1 >= 0) and (y1 >= 0):
                baseline[y1, x1] = weight
                # print(baseline)
                if current_board[y1, x1] != 0:
                    break
        except IndexError:
            pass
    # lower right
    for i in range(0, 8):
        try:
            x1 = x + i
            y1 = y + i
            if (x1 == x) and (y1 == y):
                continue
            if (x1 >= 0) and (y1 >= 0):
                baseline[y1, x1] = weight
                # print(baseline)
                if current_board[y1, x1] != 0:
                    break
        except IndexError:
            pass
    # upper right
    for i in range(0, 8):
        try:
            x1 = x + i
            y1 = y - i
            if (x1 == x) and (y1 == y):
                continue
            if (x1 >= 0) and (y1 >= 0):
                baseline[y1, x1] = weight
                # print(baseline)
                if current_board[y1, x1] != 0:
                    break
        except IndexError:
            pass
    baseline[y, x] = 0
    return baseline


def queen(index, weight=1.0, current_board=np.zeros((8, 8), dtype=np.float)):
    """
    Calculates the area of effect and weight of effect for a Queen at a particular
    index on the board.
    :param index: The position of the piece on the board
    :param weight: The weight the piece can put on the board
    :param current_board: The current chess board as a 8x8 matrix. This is used to calculate piece limits
    :return: 8x8 Matrix with piece weights.
    """
    baseline = bishop(index, weight, current_board)
    baseline += rook(index, weight, current_board)
    return baseline


def king(index, weight=1.0):
    """
    Calculates the area of effect and weight of effect for a King at a particular
    index on the board.
    :param index: The position of the piece on the board
    :param weight: The weight the piece can put on the board
    :return: 8x8 Matrix with piece weights.
    """
    baseline = np.zeros((8, 8), dtype=np.float)
    y = index[0]
    x = index[1]
    try:
        x1 = x + 1
        y1 = y
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    try:
        x1 = x + 1
        y1 = y + 1
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    try:
        x1 = x
        y1 = y + 1
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    try:
        x1 = x + 1
        y1 = y + 1
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    try:
        x1 = x - 1
        y1 = y - 1
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    try:
        x1 = x
        y1 = y - 1
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    try:
        x1 = x - 1
        y1 = y
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    try:
        x1 = x - 1
        y1 = y + 1
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    try:
        x1 = x + 1
        y1 = y - 1
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    baseline[y, x] = 0
    return baseline


def pawn(index, weight=1.0, color='WPawn'):
    """
    Calculates the area of effect and weight of effect for a King at a particular
    index on the board.
    :param index: The position of the piece on the board
    :param weight: The weight the piece can put on the board
    :param color: Expected to be WPawn or BPawn. Used to determine the orientation of the pawn
    :return: 8x8 Matrix with piece weights.
    """
    baseline = np.zeros((8, 8), dtype=np.float)
    x = index[0]
    y = index[1]
    if color == "WPawn":
        try:
            x1 = x - 1
            y1 = y + 1
            if (x1 >= 0) and (y1 >= 0):
                baseline[x1, y1] = weight
        except IndexError:
            pass
        try:
            x1 = x - 1
            y1 = y - 1
            if (x1 >= 0) and (y1 >= 0):
                baseline[x1, y1] = weight
        except IndexError:
            pass
    else:
        try:
            x1 = x + 1
            y1 = y - 1
            if (x1 >= 0) and (y1 >= 0):
                baseline[x1, y1] = weight
        except IndexError:
            pass
        try:
            x1 = x + 1
            y1 = y + 1
            if (x1 >= 0) and (y1 >= 0):
                baseline[x1, y1] = weight
        except IndexError:
            pass
    baseline[y, x] = 0
    return baseline


def knight(index, weight=1.0):
    """
    Calculates the area of effect and weight of effect for a King at a particular
    index on the board.
    :param index: The position of the piece on the board
    :param weight: The weight the piece can put on the board
    :return: 8x8 Matrix with piece weights.
    """
    baseline = np.zeros((8, 8), dtype=np.float)
    y = index[0]
    x = index[1]
    try:
        # bottom right
        x1 = x + 1
        y1 = y + 2
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    try:
        # bottom left
        x1 = x - 1
        y1 = y + 2
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass

    try:
        # upper right
        x1 = x + 1
        y1 = y - 2
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    try:
        # upper left
        x1 = x - 1
        y1 = y - 2
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    # right top
    try:
        x1 = x + 2
        y1 = y - 1
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    # right bottom
    try:
        x1 = x + 2
        y1 = y + 1
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass

    # left top
    try:
        x1 = x - 2
        y1 = y - 1
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    # left bottom
    try:
        x1 = x - 2
        y1 = y + 1
        if (x1 >= 0) and (y1 >= 0):
            baseline[y1, x1] = weight
    except IndexError:
        pass
    baseline[y, x] = 0
    return baseline


def board_eval(current_board=np.zeros((8, 8), dtype=np.float)):
    """
    Use the chess attack functions above to evaluate the board and return the pressures exerted
    by each player
    :param current_board: The current chess board as an 8x8 matrix
    :return: A tuple with pressures scaled and not scaled for each square
    """
    base_result = np.zeros((8, 8), dtype=np.float)
    valued_result = np.zeros((8, 8), dtype=np.float)

    for i in range(0, 8):
        for j in range(0, 8):
            index = (i, j)
            piece = str(current_board[i, j])
            if piece == '0':
                continue
            name = pieces[piece]['name']
            base = float(pieces[piece]['base'])
            value = 1 / (float(pieces[piece]['value']) * base)
            if piece in ['1', '11']:
                base_result += rook(index, weight=base, current_board=current_board)
                valued_result += rook(index, weight=value, current_board=current_board)
            elif piece in ['2', '12']:
                base_result += knight(index, weight=base)
                valued_result += knight(index, weight=value)
            elif piece in ['3', '6', '13', '16']:
                base_result += bishop(index, weight=base, current_board=current_board)
                valued_result += bishop(index, weight=value, current_board=current_board)
            elif piece in ['4', '14']:
                base_result += queen(index, weight=base, current_board=current_board)
                valued_result += queen(index, weight=value, current_board=current_board)
            elif piece in ['5', '15']:
                base_result += king(index, weight=base)
                valued_result += king(index, weight=value)
            elif piece in ['9', '10']:
                base_result += pawn(index, weight=base, color=name)
                valued_result += pawn(index, weight=value, color=name)
    return base_result, valued_result


def calculate_relative_color_percentiles(board):
    """
    Normalizes the pressures into a value between 0 and 1 that is used by the web app to set square darkness.
    The max and minimum is between both players, so if a player has a lot of pressure on one square, the other
    squares will look lighter for both players.
    :param board: Takes in an 8x8 matrix that represents the chessboard.
    :return:A matrix of values between 1 and 0
    """
    color = np.zeros((8, 8), dtype=np.float)
    board_vals = board.reshape(1, 64)
    board_vals = np.abs(board_vals)
    board_vals = board_vals[board_vals != 0]
    for r in range(0, 8):
        for c in range(0, 8):
            board_val = board[r, c]
            if board_val == 0:
                continue
            else:
                color[r, c] = stats.percentileofscore(board_vals, abs(board_val)) / 100
    return color


def calculate_individual_color_percentiles(board):
    """
    Normalizes the pressures into a value between 0 and 1 that is used by the web app to set square darkness.
    :param board: Takes in an 8x8 matrix that represents the chessboard.
    :return:A matrix of values between 1 and 0
    """
    color = np.zeros((8, 8), dtype=np.float)
    board_vals = board.reshape(1, 64)
    black_vals = np.abs(board_vals[board_vals < 0])
    white_vals = np.abs(board_vals[board_vals > 0])
    for r in range(0, 8):
        for c in range(0, 8):
            board_val = board[r, c]
            if board_val == 0:
                continue
            elif board_val < 0:
                color[r, c] = stats.percentileofscore(black_vals, abs(board_val)) / 100
            elif board_val > 0:
                color[r, c] = stats.percentileofscore(white_vals, abs(board_val)) / 100
    return color


def translate(board_layout):
    """
    Translates the text based notation to a numeric one used by some of the other functions in this file.
    :param board_layout: A string representation of the board.
    :return: 8x8 integer matrix
    """
    layout = board_layout
    layout = layout.replace('\n', ' ')
    layout = layout.replace('  ', ' ')
    layout = layout.replace('.', '0')
    layout = layout.replace('r', '1')
    layout = layout.replace('n', '2')
    layout = layout.replace('b', '3')
    layout = layout.replace('q', '4')
    layout = layout.replace('k', '5')
    layout = layout.replace('p', '9')
    layout = layout.replace('R', '11')
    layout = layout.replace('N', '12')
    layout = layout.replace('B', '13')
    layout = layout.replace('Q', '14')
    layout = layout.replace('K', '15')
    layout = layout.replace('P', '10')
    return np.array(layout.split(' '), dtype=np.int).reshape((8, 8))


def reverse_translation(int_val):
    """
    Translates the numeric representation of a piece to the string based representation.
    :param int_val: A numeric representation of a piece .
    :return: A single character
    """
    if int_val == 0:
        return '.'
    elif int_val == 1:
        return 'r'
    elif int_val == 2:
        return 'n'
    elif int_val == 3:
        return 'b'
    elif int_val == 4:
        return 'q'
    elif int_val == 5:
        return 'k'
    elif int_val == 6:
        return 'b'
    elif int_val == 9:
        return 'p'
    elif int_val == 11:
        return 'R'
    elif int_val == 12:
        return 'N'
    elif int_val == 13:
        return 'B'
    elif int_val == 14:
        return 'Q'
    elif int_val == 15:
        return 'K'
    elif int_val == 16:
        return 'B'
    elif int_val == 10:
        return 'P'


def create_board_from_positions(position):
    """
    Translates a chess matrix into a Board Object defined in the Chess module
    :param position: A matrix of piece positions
    :return: Chess Board object
    """
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    board = chess.Board()
    board.clear_board()
    for index, value in enumerate(files):
        for row in range(0, 8):
            if position[row, index] == 0:
                continue
            board.set_piece_at(chess.parse_square(value + str(8 - row)),
                               chess.Piece.from_symbol(reverse_translation(position[row, index])))
            # print('({},{}, {}) = {}'.format(row, index, position[row,index], value + str(8-row)))
    return board


def recommend_black(board, model):
    """
    Uses a learned model and a chess board object to recommend the move that maximizes pressure and the 'winning'
    move categorized by the model
    :param model: The model for classification
    :param board: Loaded Chess Board Object
    :return: Move to maximize pressure, pressure of that move, ML recommended move, Model classification for that move
    """
    board.turn = chess.BLACK
    moves = board.legal_moves
    rec_list = []
    for move in moves:
        board.push_uci(str(move))
        positions = translate(str(board))
        base, val = board_eval(positions)
        percents = calculate_relative_color_percentiles(val)
        board_percents = np.dstack(val)
        ml = model.predict(board_percents)[0, 0] * 100
        value = np.sum(percents)
        rec_list.append({'move': str(move), 'value': value, 'ml': ml})
        board.pop()
    rec = rec_list[0]['move']
    rec_val = rec_list[0]['value']

    for index in range(1, len(rec_list)):
        if rec_list[index]['value'] < rec_val:
            rec = rec_list[index]['move']
            rec_val = rec_list[index]['value']
    board.push_uci(rec)

    rec_ml = rec_list[0]['move']
    rec_val_ml = rec_list[0]['ml']

    for index in range(1, len(rec_list)):
        if rec_list[index]['ml'] < rec_val_ml:
            rec_ml = rec_list[index]['move']
            rec_val_ml = rec_list[index]['ml']

    return rec, rec_val, rec_ml, abs(rec_val_ml)


def recommend_white(board, model):
    """
    Uses a learned model and a chess board object to recommend the move that maximizes pressure and the 'winning'
    move categorized by the model
    :param model: The model for classification
    :param board: Loaded Chess Board Object
    :return: Move to maximize pressure, pressure of that move, ML recommended move, Model classification for that move
    """
    board.turn = chess.WHITE
    moves = board.legal_moves
    rec_list = []
    for move in moves:
        board.push_uci(str(move))
        positions = translate(str(board))
        base, val = board_eval(positions)
        percents = calculate_relative_color_percentiles(val)
        board_percents = np.dstack(val)
        ml = model.predict(board_percents)[0, 0] * 100
        value = np.sum(percents)
        rec_list.append({'move': str(move), 'value': value, 'ml': ml})
        board.pop()
    rec = rec_list[0]['move']
    rec_val = rec_list[0]['value']

    for index in range(1, len(rec_list)):
        if rec_list[index]['value'] > rec_val:
            rec = rec_list[index]['move']
            rec_val = rec_list[index]['value']
    board.push_uci(rec)

    rec_ml = rec_list[0]['move']
    rec_val_ml = rec_list[0]['ml']

    for index in range(1, len(rec_list)):
        if rec_list[index]['ml'] > rec_val_ml:
            rec_ml = rec_list[index]['move']
            rec_val_ml = rec_list[index]['ml']

    return rec, rec_val, rec_ml, abs(rec_val_ml)
