import random

def print_board(board):
    markers = '? 123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for row in board:
        for cell in row:
            print markers[cell],
        print

def fill_rectangle(board, left, top, width, height, block):
    if width <= 0 or height <= 0:
        return block

    if height % 2 == 1:
        for x in xrange(left, left + width, 2):
            board[top][x] = board[top][x + 1] = block
            block += 1

        top += 1
        height -= 1

    for y in xrange(top, top + height, 2):
        for x in xrange(left, left + width):
            board[y][x] = board[y + 1][x] = block
            block += 1

    # print_board(board)
    # print '-' * 20
    return block

def fill_board(x1, y1, x2, y2):
    assert 0 <= x1 <= 7 and 0 <= y1 <= 7 and 0 <= x2 <= 7 and 0 <= y2 <= 7
    if (x1 + y1) % 2 == (x2 + y2) % 2:
        return False

    n = 8
    board = [[0] * n for _ in xrange(n)]
    block = 1

    board[y1][x1] = board[y2][x2] = block
    block += 1

    left = min(x1, x2)
    right = max(x1, x2)
    top = min(y1, y2)
    bottom = max(y1, y2)
    width = right - left + 1
    height = bottom - top + 1
    print (left, top), '-', (right, bottom)
    print width, 'x', height

    if (x1 == left and y1 == top) or (x2 == left and y2 == top):
        offset = (1, 0)
    else:
        offset = (0, 1)

    if height % 2 == 1:
        block = fill_rectangle(board, left, top + offset[0], 1, height - 1, block)
        block = fill_rectangle(board, right, top + offset[1], 1, height - 1, block)
        block = fill_rectangle(board, left + 1, top, width - 2, height, block)
        block = fill_rectangle(board, left, 0, width, top, block)
        block = fill_rectangle(board, left, bottom + 1, width, n - bottom - 1, block)
        block = fill_rectangle(board, 0, 0, left, n, block)
        block = fill_rectangle(board, right + 1, 0, n - right - 1, n, block)
    else:
        block = fill_rectangle(board, left + offset[0], top, width - 1, 1, block)
        block = fill_rectangle(board, left + offset[1], bottom, width - 1, 1, block)
        block = fill_rectangle(board, left, top + 1, width, height - 2, block)
        block = fill_rectangle(board, 0, 0, n, top, block)
        block = fill_rectangle(board, 0, bottom + 1, n, n - bottom - 1, block)
        block = fill_rectangle(board, 0, top, left, height, block)
        block = fill_rectangle(board, right + 1, top, n - right - 1, height, block)

    return board

def demo():
    x1 = random.randint(0, 7)
    y1 = random.randint(0, 7)
    x2 = random.randint(0, 7)
    y2 = random.randint(0, 7)
    print (x1, y1), (x2, y2)
    board = fill_board(x1, y1, x2, y2)
    if board:
        print_board(board)
    else:
        print False
