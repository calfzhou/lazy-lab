class MinStack:
    def __init__(self):
        self._stack = []

    def push(self, item):
        index = len(self._stack)
        if self._stack:
            min_item, min_index = self.min()
            if item >= min_item:
                index = min_index

        self._stack.append((item, index))

    def pop(self):
        item, _ = self._stack.pop()
        return item

    def __len__(self):
        return len(self._stack)

    def __iter__(self):
        for item, _ in self._stack:
            yield item

    def __getitem__(self, i):
        return self._stack[i][0]

    def min(self):
        if len(self) > 0:
            _, min_index = self._stack[-1]
            return self._stack[min_index]
        else:
            return None

    def __repr__(self):
        return repr(self._stack)
