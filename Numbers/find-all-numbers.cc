// Copyright 2007 All Rights Reserved.
// Author: Ji Zhou

#include <iostream>
#include <vector>
#include <algorithm>
#include <assert.h>

using std::vector;
using std::sort;

typedef unsigned long NumberType;
typedef vector<NumberType> NumberVector;

const int MAX_EXP_DIGITS = 9;
const NumberType EXP_VALUES[MAX_EXP_DIGITS + 1] = {
  1UL,
  10UL,
  100UL,
  1000UL,
  10000UL,
  100000UL,
  1000000UL,
  10000000UL,
  100000000UL,
  1000000000UL
};

inline NumberType Exp(int n) {
  assert(0 <= n && n <= MAX_EXP_DIGITS);
  return EXP_VALUES[n];
}

void NumberInfo(
    const NumberType &number,
    int &exp_digits,
    NumberType &head_digit,
    NumberType &remain_number) {
  assert(number > 0);
  for (exp_digits = MAX_EXP_DIGITS;
       Exp(exp_digits) > number;
       --exp_digits) {
  }

  remain_number = number;
  const NumberType &exp_number = Exp(exp_digits);
  for (head_digit = 0; remain_number >= exp_number; ++head_digit) {
    remain_number -= exp_number;
  }
}

NumberType CountOnes(const NumberType &number) {
  if (number == 0) return 0;
  
  int exp_digits;
  NumberType head_digit;
  NumberType remain_number;

  NumberInfo(number, exp_digits, head_digit, remain_number);
  if (exp_digits == 0) return 1;
  
  NumberType ones = CountOnes(remain_number);
  ones += head_digit * exp_digits * Exp(exp_digits - 1);
  ones += ((head_digit > 1) ? Exp(exp_digits) : (remain_number + 1));
  return ones;
}

NumberType FindToBigger(
    NumberType number,
    const NumberType &limit,
    NumberVector &valid_numbers
    ) {
  while (0 < number && number <= limit) {
    NumberType ones = CountOnes(number);
    //std::cout << "------: f(" << number << ") = " << ones << "\n";
    if (number == ones) {
      valid_numbers.push_back(number);
      number = ones + 1;
    }
    else if (number < ones) {
      number = ones;
    }
    else {
      break;
    }
  }
  return number + 1;
}

NumberType FindToSmaller(
    NumberType number,
    const NumberType &limit,
    NumberVector &valid_numbers) {
  while (number >= limit) {
    NumberType ones = CountOnes(number);
    //std::cout << "------: f(" << number << ") = " << ones << "\n";
    if (number == ones) {
      valid_numbers.push_back(number);
      number = ones - 1;
    }
    else if (number > ones) {
      number = ones;
    }
    else {
      break;
    }
  }
  return number - 1;
}

void FindAllHelper(
    NumberType small_number,
    NumberType big_number,
    NumberVector &valid_numbers) {
  if (small_number <= big_number)
    small_number = FindToBigger(small_number, big_number, valid_numbers);

  if (small_number <= big_number)
    big_number = FindToSmaller(big_number, small_number, valid_numbers);

  if (small_number <= big_number) {
    NumberType middle_number = (small_number + big_number) / 2;
    FindAllHelper(small_number, middle_number, valid_numbers);
    FindAllHelper(middle_number + 1, big_number, valid_numbers);
  }
}

void FindAll(const NumberType &number, NumberVector &valid_numbers) {
  valid_numbers.clear();
  FindAllHelper(1, number, valid_numbers);
  sort(valid_numbers.begin(), valid_numbers.end());
}

int main()
{
  NumberType number = 2111111100;
  NumberVector valid_numbers;

  FindAll(number, valid_numbers);
  for (NumberVector::const_iterator it = valid_numbers.begin();
       it != valid_numbers.end();
       ++it) {
    std::cout << "f(" << *it << ")=" << *it << "\n";
  }
  return 0;
}
