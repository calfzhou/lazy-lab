// Copyright 2007. All Rights Reserved.
// Author: Ji Zhou
#include <iostream>
#include <vector>

using namespace std;

// 求数组array的平衡点left_size（即array左边left_size个数字之和与
// 其余数字之和相等。若找到平衡点，返回真。
bool Foo(const vector<int> &array, int &left_size) {
  if (array.size() < 2) return false;
  vector<int>::const_iterator it_l = array.begin();
  vector<int>::const_iterator it_r = array.end() - 1;
  int val_l = 0;
  int val_r = 0;
  while (it_l <= it_r) {
    if (val_l == 0) { val_l = *it_l++; }
    else if (val_r == 0) { val_r = *it_r--; }
    else if (val_l <= val_r) { val_r -= val_l; val_l = 0; }
    else { val_l -= val_r; val_r = 0; }
  }
  left_size = it_l - array.begin();
  return val_l == val_r;
}

int main() {
  vector<int> array;
  int num;
  while (cin >> num && num >= 0)
    array.push_back(num);
  cout << "Accepted array: [";
  for (vector<int>::const_iterator it = array.begin(); it != array.end(); ) {
    cout << *it;
    if (++it != array.end())  cout << ", ";
  }
  cout << "]" << endl;

  int balance_point;
  if (Foo(array, balance_point)) {
    cout << "One balance point: " << balance_point << endl;
  } else {
    cout << "No balance point." << endl;
  }

  return 0;
}
