#!/usr/bin/python2.4
#
# Copyright 2007. All Rights Reserved.

"""One-line documentation for balance module.

A detailed description of balance.
"""

__author__ = 'Ji Zhou'


def BalancePoints(li):
  """Find all balance points of 'li'.

  Args:
    li: A list or a tuple of at most 1G integers.

  Returns:
    A list of balance points (sort ascending).
  """
  total_sum = 0
  for i in range(len(li)):
    total_sum += li[i]

  left_sum = 0
  balance_points = []
  for i in range(len(li) - 1):
    left_sum += li[i] * 2
    if left_sum == total_sum:
      balance_points.append(i + 1)

  return balance_points


def Main():
  li = []
  try:
    while True:
      li.append(int(raw_input()))
  except ValueError:
    pass
  except EOFError:
    pass

  balance_points = BalancePoints(li)
  print 'Balance points:', repr(balance_points)


if __name__ == '__main__':
  Main()
