#!/usr/bin/python2.4
#
# Copyright 2007 All Rights Reserved.

"""One-line documentation for count_ones module.

A detailed description of count_ones.
"""

__author__ = 'Ji Zhou'

class InvalidIntegerError(Exception): pass

def NumberInfo(number):
  if not number >= 0: raise InvalidIntegerError, "%s is not >= 0" % str(number)
  if int(number) <> number: raise InvalidIntegerError, \
      "%s is not an integer" % str(number)
  
  number_string = str(number)
  return (len(number_string) - 1, int(number_string[0]), int('0' + number_string[1:]))


CountOnesForNines = lambda nine_digits: nine_digits * int(10 ** (nine_digits - 1))


def CountOnes(number):
  (exp_digits, head_digit, remain_number) = NumberInfo(number)
  if not exp_digits: return head_digit and 1 or 0
  ones_count = head_digit * CountOnesForNines(exp_digits) + CountOnes(remain_number)
  ones_count += head_digit > 1 and (10 ** exp_digits) or remain_number + 1
  return ones_count


if __name__ == '__main__':
  import sys
  print CountOnes(int(sys.argv[-1]))
