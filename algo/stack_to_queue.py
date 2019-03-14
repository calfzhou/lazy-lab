class Queue:
    def __init__(self):
        self._s1 = []
        self._s2 = []

    def push(self, item):
        self._s1.append(item)

    def pop(self):
        if not self._s2:
            while self._s1:
                self._s2.append(self._s1.pop())

        return self._s2.pop()

    def __len__(self):
        return len(self._s1) + len(self._s2)

    def __repr__(self):
        first_part = ', '.join('%s' % item for item in reversed(self._s2))
        last_part = ', '.join('%s' % item for item in self._s1)
        return '[%s]' % ' | '.join([first_part, last_part])
