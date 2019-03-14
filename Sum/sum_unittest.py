"""Unit test for sum.py
"""

import sum
import unittest
from random import Random


_INT_CNT_RANGE = range(1, 10)


class BasicValues(unittest.TestCase):
  def testSum(self):
    """Test with basic zero-one values.
    """
    for n in _INT_CNT_RANGE:
      fn_norm = sum.GenerateNormalFunction(n)
      fn_spec = sum.GenerateSpecialFunction(n)
      for ones_cnt in range(n+1):
        a = [ii<ones_cnt and 1 or 0 for ii in range(n)]
        s_norm = fn_norm(a)
        s_spec = fn_spec(a)
        self.assertEqual(s_norm, s_spec,
            'a=%s, s_norm=%d, s_spec=%d' % (str(a), s_norm, s_spec))


class RandomValues(unittest.TestCase):
  def testSum(self):
    """Test with random values.
    """
    test_cnt = 100
    rand = Random()
    rand.seed()
    while test_cnt > 0:
      test_cnt -= 1
      n = rand.choice(_INT_CNT_RANGE)
      fn_norm = sum.GenerateNormalFunction(n)
      fn_spec = sum.GenerateSpecialFunction(n)
      a = [rand.randint(0, 32768) for i in range(n)]
      s_norm = fn_norm(a)
      s_spec = fn_spec(a)
      self.assertEqual(s_norm, s_spec,
          'a=%s, s_norm=%d, s_spec=%d' % (str(a), s_norm, s_spec))


if __name__ == "__main__":
  unittest.main()
