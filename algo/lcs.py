def get_indexes(s, i, j):
    d = s[i][j]
    if d == 0:
        sub = get_indexes(s, i - 1, j - 1)
        sub.append(i)
        return sub
    elif d == 1:
        return get_indexes(s, i - 1, j)
    elif d == 2:
        return get_indexes(s, i, j - 1)
    else:
        return []

def get_indexes_loop(s, i, j):
    while True:
        d = s[i][j]
        if d == 0:
            yield i
            i -= 1
            j -= 1
        elif d == 1:
            i -= 1
        elif d == 2:
            j -= 1
        else:
            raise StopIteration

def lcs(list1, list2):
    m = len(list1)
    n = len(list2)
    c = [[0] * (n + 1) for _ in xrange(m + 1)]
    s = [[None] * (n + 1) for _ in xrange(m + 1)]

    for i, x in enumerate(list1, 1):
        for j, y in enumerate(list2, 1):
            if x == y:
                c[i][j] = c[i - 1][j - 1] + 1
                s[i][j] = 0
            else:
                if c[i - 1][j] >= c[i][j - 1]:
                    c[i][j] = c[i - 1][j]
                    s[i][j] = 1
                else:
                    c[i][j] = c[i][j - 1]
                    s[i][j] = 2

    print c[m][n]
    # indexes = get_indexes(s, m, n)
    # return ' '.join(list1[i - 1] for i in indexes)
    seq = [list1[i - 1] for i in get_indexes_loop(s, m, n)]
    return ' '.join(reversed(seq))

def demo():
    x = 'ABCBDAB'
    y = 'BDCABA'
    print lcs(x, y)
