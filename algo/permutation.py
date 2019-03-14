def permutation(array, mask=None, result=None):
    if mask is None:
        mask = [False] * len(array)
        result = []
    elif False not in mask:
        # print ''.join(result)
        yield result
        return

    for i, x in enumerate(array):
        if mask[i]:
            continue

        result.append(x)
        mask[i] = True
        for x in permutation(array, mask, result):
            yield x
        mask[i] = False
        result.pop()

def combination(array, n, offset=0, result=None):
    if result is None:
        result = []
    elif n == 0:
        # print ''.join(result)
        yield result
        return
    elif offset >= len(array):
        return

    for i in xrange(offset, len(array)):
        result.append(array[i])
        for x in combination(array, n - 1, i + 1, result):
            yield x
        result.pop()
