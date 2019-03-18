
def MinInnerProduct(A, B, n, s):
  if not len(A) == len(B) == n or not 0 <= s <= n:
    raise Exception('Invalid arguments.')

  A.sort()
  B.sort()
  (C, D, sum) = ([], [], 0)
  (i, j) = (0, n - 1)

  while len(C) < s:
    val1 = A[i] * B[i]
    val2 = A[j] * B[j]
    if val1 < 0 and val2 < 0:
      break
    if val1 >= val2:
      C.append(A[i])
      D.append(B[i])
      sum += val1
      i += 1
    else:
      C.append(A[j])
      D.append(B[j])
      sum += val2
      j -= 1

  j -= s - len(C) - 1
  while len(C) < s:
    C.append(A[i])
    D.append(B[j])
    sum += A[i] * B[j]
    i += 1
    j += 1

  return (C, D, sum)

from random import Random

rand = Random()

def Foo():
  A = [-15, -4, 1, 2, 3, 7, 10]
  B = [-7, -6, -4, -2, -1, 8, 9]
  rand.shuffle(A)
  rand.shuffle(B)
  n = len(A)
  print 'A =', A
  print 'B =', B
  for i in xrange(n):
    s = i + 1
    (C, D, sum) = MinInnerProduct(A, B, n, s)
    print
    print 's =', s, 'sum =', sum
    print 'C =', C
    print 'D =', D


Foo()
