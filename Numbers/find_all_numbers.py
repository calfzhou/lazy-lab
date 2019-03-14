#!/usr/bin/python2.4
#
# Copyright 2007 All Rights Reserved.

"""One-line documentation for find_all_numbers module.

A detailed description of find_all_numbers.
"""

__author__ = 'Ji Zhou'

from count_ones import CountOnes

is_debug = False #or True


def FindToBigger(number, limit, stop_at):
  while 0 < number <= limit:
    count = CountOnes(number)
    if is_debug: print 'f(%d)=%d' % (number, count)
    if number == count:
      yield number
      number = count + 1
    elif number < count:
      number = count
    else:
      break
  
  stop_at[0] = number + 1


def FindToSmaller(number, limit, stop_at):
  while number >= limit:
    count = CountOnes(number)
    if is_debug: print 'f(%d)=%d' % (number, count)
    if number == count:
      yield number
      number = count - 1
    elif number > count:
      number = count
    else:
      break
  
  stop_at[0] = number - 1


def FindAllHelper(small_number, big_number):
  stop_at = [None]
  
  if small_number <= big_number:
    for n in FindToBigger(small_number, big_number, stop_at): yield n
    small_number = stop_at[0]
  
  if small_number <= big_number:
    for n in FindToSmaller(big_number, small_number, stop_at): yield n
    big_number = stop_at[0]
  
  if small_number <= big_number:
    middle_number = (small_number + big_number) / 2
    for n in FindAllHelper(small_number, middle_number): yield n
    for n in FindAllHelper(middle_number + 1, big_number): yield n


def FindAll(number):
  finder = FindAllHelper(1, number)
  numbers = []
  for n in finder: numbers.append(n)
  return numbers


if __name__ == '__main__':
  import sys
  numbers = FindAll(int(sys.argv[-1]))
  numbers.sort()
  for n in numbers:
    print 'f(%d)=%d' % (n, n)
