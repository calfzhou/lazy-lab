def calc_bin_tree_count(n):
    if n < 0:
        return

    cache = [None] * (n + 1)
    cache[0] = 1
    for m in xrange(1, n + 1):
        count = 0
        for k in xrange(0, m):
            count += cache[k] * cache[m - 1 - k]
        cache[m] = count

    return cache[-1]
