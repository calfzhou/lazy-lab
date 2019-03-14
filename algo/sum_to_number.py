import random
import math

class Prime:
    def __init__(self):
        self._primes = [2, 3, 5, 7]

    def __iter__(self):
        for n in self._primes:
            yield n

        n = self._primes[-1]
        while True:
            n += 2
            sqrt_n = int(math.sqrt(n))
            is_prime = True
            for p in self._primes:
                if p > sqrt_n:
                    break
                if n % p == 0:
                    is_prime = False
                    break

            if is_prime:
                self._primes.append(n)
                yield n

primes = Prime()

def factors(num):
    for p in primes:
        if p > num:
            break

        while num % p == 0:
            yield p
            num /= p

def factors_2x(num):
    special = 2
    for p in factors(num):
        if p == 2:
            special *= p
        else:
            if special is not None and special < p:
                yield special
                special = None
            yield p

def split_number(num):
    n = 1
    while True:
        n += 1
        if n % 2 == 0:
            nk = num - n / 2 * (n - 1)
        else:
            nk = num - (n - 1) / 2 * n

        if nk < n:
            break

        if nk % n != 0:
            continue

        k = nk / n
        print k, n
        assert sum(xrange(k, k + n)) == num
