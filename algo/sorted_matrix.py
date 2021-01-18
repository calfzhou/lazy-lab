import random

def build_matrix(width, height):
    matrix = [[None] * width for _ in xrange(height)]
    value = iter(xrange(1, width * height + 1))
    positions = [(0, height - 1)]

    while positions:
        x0, y0 = positions.pop(random.randint(0, len(positions) - 1))
        matrix[y0][x0] = value.next()
        all_x = {x for x, _ in positions}
        all_y = {y for _, y in positions}
        if y0 - 1 >= 0 and (y0 - 1) not in all_y:
            positions.append((x0, y0 - 1))
        if x0 + 1 < width and (x0 + 1) not in all_x:
            positions.append((x0 + 1, y0))

    return matrix

def verify_matrix(matrix):
    height = len(matrix)
    width = len(matrix[0])

    for y in xrange(height):
        prev = matrix[y][0]
        for x in xrange(1, width):
            assert matrix[y][x] >= prev
            prev = matrix[y][x]

    for x in xrange(width):
        prev = matrix[0][x]
        for y in xrange(1, height):
            assert matrix[y][x] <= prev
            prev = matrix[y][x]

def print_matrix(matrix):
    for row in matrix:
        for value in row:
            print '%2d' % value,
        print

def find_k_min(matrix, k):
    height = len(matrix)
    width = len(matrix[0])
    assert 1 <= k <= width * height
    # TODO: 可以用大顶堆维护候选位置
    positions = {(0, height - 1)}

    for _ in xrange(k):
        x0, y0 = min(positions, key=lambda p: matrix[p[1]][p[0]])
        positions.remove((x0, y0))
        all_x = {x for x, _ in positions}
        all_y = {y for _, y in positions}
        if y0 - 1 >= 0 and (y0 - 1) not in all_y:
            positions.add((x0, y0 - 1))
        if x0 + 1 < width and (x0 + 1) not in all_x:
            positions.add((x0 + 1, y0))

    return matrix[y0][x0]

def find_value(matrix, value):
    height = len(matrix)
    width = len(matrix[0])
    x = y = 0
    while x < width and y < height:
        curr = matrix[y][x]
        if value == curr:
            return x, y
        elif value < curr:
            y += 1
        else:
            x += 1
    return False

def demo():
    width = random.randint(5, 12)
    height = random.randint(70, 99) / width
    total = width * height
    print width, 'x', height, '=', total
    matrix = build_matrix(width, height)
    print_matrix(matrix)

    print 'Verifying matrix ...'
    verify_matrix(matrix)

    print 'Testing find_k_min ...'
    for k in xrange(1, total + 1):
        k_min = find_k_min(matrix, k)
        if k_min != k:
            print 'min(matrix, %d) = %d' % (k, k_min)

    print 'Testing find_value ...'
    for value in xrange(int(total * 1.2)):
        res = find_value(matrix, value)
        if res is False:
            if 0 < value <= total:
                print 'Error: cannot find', value
        else:
            x, y = res
            if matrix[y][x] != value:
                print 'Error: found', value, 'at', (x, y), '=', matrix[y][x]

def main():
    width = 8
    height = 9
    matrix = build_matrix(width, height)
    print_matrix(matrix)
    k = 20
    k_min = find_k_min(matrix, k)
    print 'min(matrix, %d) = %d' % (k, k_min)

if __name__ == '__main__':
    main()
