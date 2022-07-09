#!/usr/bin/env python3


def enumerate_complete_circles(n: int):
    numbers = set(range(1, n + 1))
    arrangement = [None] * n

    def _put(pos=0, step=0):
        # `pos` equals `sum(filter(None, arrangement)) % n`
        # `step` equals `len(list(filter(None, arrangement)))`
        if step == n:
            yield arrangement
            return

        if arrangement[pos] is not None:
            return

        for num in numbers - set(arrangement):
            arrangement[pos] = num
            next_pos = (pos + num) % n
            yield from _put(next_pos, step + 1)

        arrangement[pos] = None

    yield from _put()


def main():
    for arrangement in enumerate_complete_circles(6):
        print(arrangement)


if __name__ == '__main__':
    main()
