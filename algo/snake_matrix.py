import random

def build_matrix(width, height):
    matrix = [[None] * width for _ in xrange(height)]
    value = iter(xrange(1, width * height + 1))

    for y in xrange(height + width):
        direction = y % 2
        endx = min(y + 1, width)
        if y >= height:
            x = y - (height - 1)
            y = height - 1
        else:
            x = 0

        if direction == 1:
            for x in xrange(x, endx):
                matrix[y][x] = value.next()
                y -= 1
        else:
            y -= endx - x - 1
            for x in xrange(endx - 1, x - 1, -1):
                matrix[y][x] = value.next()
                y += 1

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
