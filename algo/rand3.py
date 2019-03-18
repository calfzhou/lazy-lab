from random import Random

def Rand5():
  return Random().randint(0, 4)

def Rand3():
  x = -1
  while not 0 <= x < 3:
    x = Rand5()
  return x

def Rand7():
  x = -1
  while not 0 <= x < 21:
    x = Rand5() * 5 + Rand5()
  return x % 7

def RandM(m):
  return Random().randint(0, m - 1)

def RandN(n, m):
  k = 1
  mk = m
  while mk < n:
    k += 1
    mk  *= m
  c = mk / n
  cn = c * n
  x = -1
  while not 0 <= x < cn:
    x = 0
    for idx in xrange(k):
      x = x * m + RandM(m)
  return x % n

if __name__ == '__main__':
  print [RandN(7, 5) for i in xrange(20)]
