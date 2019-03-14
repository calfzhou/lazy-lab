from min_stack import MinStack

class MinQueue:
    def __init__(self):
        self._s1 = MinStack()
        self._s2 = MinStack()

    def push(self, item):
        self._s1.push(item)

    def pop(self):
        if not self._s2:
            while self._s1:
                self._s2.push(self._s1.pop())

        return self._s2.pop()

    def min(self):
        m1 = None
        m2 = None
        if len(self._s1) > 0:
            m1, i1 = self._s1.min()
            i1 += len(self._s2)

        if len(self._s2) > 0:
            m2, i2 = self._s2.min()
            i2 = len(self._s2) - i2 - 1

        if m1 is None and m2 is None:
            return None
        elif m1 is None:
            return m2, i2
        elif m2 is None:
            return m1, i1
        elif m1 < m2:
            return m1, i1
        else:
            return m2, i2

    def __iter__(self):
        for x in reversed(self._s2):
            yield x

        for x in self._s1:
            yield x

    def __getitem__(self, i):
        if i < len(self._s2):
            return self._s2[-1 - i]
        else:
            i -= len(self._s2)
            return self._s1[i]

    def __len__(self):
        return len(self._s1) + len(self._s2)

    def __repr__(self):
        first_part = repr(self._s1)
        last_part = repr(self._s2)
        return ' | '.join([first_part, last_part])
