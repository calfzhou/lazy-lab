import random

def build_matrix(width, height):
    matrix = [[0] * width for _ in xrange(height)]
    value = iter(xrange(1, width * height + 1))

    x = -1
    y = 0
    direction = 1
    while width > 0 and height > 0:
        for _ in xrange(width):
            x += direction
            matrix[y][x] = value.next()
        for _ in xrange(height - 1):
            y += direction
            matrix[y][x] = value.next()

        direction = 0 - direction
        width -= 1
        height -= 1

    return matrix

def print_matrix(matrix):
    for row in matrix:
        for value in row:
            print '%2d' % value,
        print

def demo():
    width = random.randint(3, 12)
    height = random.randint(80, 99) / width
    total = width * height
    print width, 'x', height, '=', total
    matrix = build_matrix(width, height)
    print_matrix(matrix)
