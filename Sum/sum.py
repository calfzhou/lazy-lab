"""Use only one '+' to add three numbers. Or use two '+'s to add atmost seven
numbers. (log n '+'s to add n numbers)
a + b = (a^b) + ((a&b) << 1)
a + b + c = (a^b^c) + ((a&b | a&c | b&c) << 1)
a + b + c + d = a^b^c^d +
                (((a&b | a&c | ...) & ~(a&b&c&d)) << 1) +
                ((a&b&c&d) << 2)

In fact, we can use only one '+' to add any count of numbers.
For example:
  a + b + c + d
  = (a + b + c) + d
  = (a^b^c) + ((a&b | a&c | b&c) << 1) + c
  = ((a^b^c) ^ ((a&b | a&c | b&c) << 1) ^ c) +
    ((.........................) << 1)

This program only implemented the first case.
"""


def GenerateNormalFunction(n):
  """Returns a functions to do normal addition.
  """
  return eval('lambda a: %s' % GenerateNormalExpression(n))


def GenerateSpecialFunction(n):
  """Returns a functions to do special addition.
  """
  return eval('lambda a: %s' % GenerateSpecialExpression(n))


def GenerateNormalExpression(n):
  """Returns the normal expression to add n non-negative integers.
  Returns None if n is not a positive integer.
  """
  if int(n) != n or n < 1:
    return None
  return '+'.join(['a[%d]' % ii for ii in range(n)])


def GenerateSpecialExpression(n):
  """Returns the special expression to add n non-negative integers.
  Returns None if n is not a positive integer.
  """
  if int(n) != n or n < 1:
    return None
  sub_exp_list = []

  # The XOR part.
  expression = '^'.join(['a[%d]' % ii for ii in range(n)])
  sub_exp_list.append(expression)

  # The carry parts (log n parts).
  carry_level = 1
  while 1<<carry_level <= n:
    carry_ones_list = range(1<<carry_level, n+1, 1<<carry_level)
    carry_exp_list = [CarryExpression(n, c) for c in carry_ones_list]
    part_exp_list = []
    for ii in range(0, len(carry_ones_list), 2):
      carry_ones = carry_ones_list[ii]
      expression = ')&~('.join(carry_exp_list[ii:])
      if len(carry_ones_list) - ii > 1:
        expression = '(%s)' % expression
      part_exp_list.append(expression)
    expression = ') | ('.join(part_exp_list)
    if len(part_exp_list) > 1:
      expression = '(%s)' % expression
    expression = '(%s) << %d' % (expression, carry_level)
    sub_exp_list.append(expression)
    carry_level += 1

  # Compose the expression.
  expression = ') + ('.join(sub_exp_list)
  if len(sub_exp_list) > 1:
    expression = '(%s)' % expression
  return expression


def Combinations(n, k):
  """Returns a list of n's k combinations.
  For example, if n = 3, k = 2, the return list is:
  [[0,1], [0,2], [1,2]]
  """
  if int(n) != n or int(k) != k or n < k or k <= 0:
    return None

  if k == n:
    return [range(n)]
  elif k == 1:
    return [[ii] for ii in range(n)]

  combinations = Combinations(n-1, k)
  combinations_append_last = Combinations(n-1, k-1)
  for ii in range(len(combinations_append_last)):
    combination = combinations_append_last[ii]
    combination.append(n-1)
    combinations.append(combination)
  return combinations


def CarryExpression(n, c):
  """Returns the expression of the c's carry of n elements.
  """
  combinations = Combinations(n, c)
  bit_and_list = []
  for ii in range(len(combinations)):
    bit_and_list.append('&'.join('a[%d]' % jj for jj in combinations[ii]))
  carry_expression = '|'.join(bit_and_list)
  return carry_expression


def main(arg):
  if not arg:
    arg = range(1, 10)
  for n in arg:
    print GenerateNormalExpression(n), '=', GenerateSpecialExpression(n)


if __name__ == "__main__":
  import sys
  arg = []
  for ii in range(1, len(sys.argv)):
    arg.append(int(sys.argv[ii]))
  main(arg)
