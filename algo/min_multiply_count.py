def format_result(s, start, end):
    if start == end:
        return 'A%d' % start

    mid = s[start][end]
    left = format_result(s, start, mid)
    right = format_result(s, mid + 1, end)
    return '(%s * %s)' % (left, right)

def matrix_chain(dims):
    n = len(dims) - 1
    m = [[0] * n for _ in xrange(n)]
    s = [[None] * n for _ in xrange(n)]

    for chain_length in xrange(2, n + 1): # [2, n]
        for start_index in xrange(n - chain_length + 1): # [0, n - chain_length]
            end_index = start_index + chain_length - 1
            chain_best = None
            for mid_index in xrange(start_index, end_index): # [start, end)
                merge = dims[start_index] * dims[mid_index + 1] * dims[end_index + 1]
                temp = m[start_index][mid_index] + m[mid_index + 1][end_index] + merge
                if chain_best is None or temp < chain_best:
                    chain_best = temp
                    s[start_index][end_index] = mid_index

            m[start_index][end_index] = chain_best

    print s
    print m[0][n - 1]
    print format_result(s, 0, n - 1)

def demo():
    dims = [30, 35, 15, 5, 10, 20, 25]
    matrix_chain(dims)
