import random

def print_board(board):
    markers = '? 123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for row in board:
        for cell in row:
            print markers[cell],
        print

def fill(board, left, top, size, x0, y0, block):
    if size == 2:
        for y in xrange(top, top + size):
            for x in xrange(left, left + size):
                if x != x0 or y != y0:
                    board[y][x] = block

        block += 1
        return block

    half_size = size / 2
    midx = left + half_size - 1
    midy = top + half_size - 1
    blockx = 0 if x0 <= midx else 1
    blocky = 0 if y0 <= midy else 1

    block = fill(board, midx, midy, 2, midx + blockx, midy + blocky, block)

    for j in xrange(2):
        for i in xrange(2):
            if blockx == i and blocky == j:
                x = x0
                y = y0
            else:
                x = midx + i
                y = midy + j

            block = fill(board, left + i * half_size, top + j * half_size, half_size, x, y, block)

    return block


def fill_board(n, x0, y0):
    assert 0 <= x0 < n and 0 <= y0 < n
    board = [[0] * n for _ in xrange(n)]
    block = 1

    board[y0][x0] = block
    block += 1
    fill(board, 0, 0, n, x0, y0, block)
    return board

def demo():
    n = 8
    x0 = random.randint(0, 7)
    y0 = random.randint(0, 7)
    print (x0, y0)
    board = fill_board(n, x0, y0)
    print_board(board)
