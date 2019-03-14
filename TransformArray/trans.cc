#include <iostream>
#include <vector>
#include <iterator>
#include <algorithm>

using namespace std;

int Trans(int x, int n) {
  if (x < n) {
    return (x << 1) + 1;
  } else {
    return (x-n) << 1;
  }
}

bool IsFirstOfAGroup(int s, int n) {
  int i = s;
  do {
    i = Trans(i, n);
    if (i < s) return false;
  } while (i != s);
  return true;
}

template <typename T>
void TransArrayStartFrom(vector<T>& array, int s, int n) {
  T tmp = array[s];
  int j = s;
  do {
    j = Trans(j, n);
    swap(array[j], tmp);
  } while (j != s);
}

template <typename T>
void TransWholeArray(vector<T>& array, int n) {
  for (int s = 0; s < n; ++s) {
    if (IsFirstOfAGroup(s, n))
      TransArrayStartFrom(array, s, n);
  }
}

bool Check(const vector<int>& array) {
  int tmp = 0;
  for (vector<int>::const_iterator it = array.begin();
       it != array.end(); ++it) {
    if (*it <= tmp) return false;
    tmp = *it;
  }
  return true;
}

int main(int argc, char** argv) {
  if (argc != 2) return -1;
  int n = atoi(argv[1]);
  vector<int> array;
  for (int i = 0; i < n; ++i) array.push_back((i<<1) + 2);
  for (int i = 0; i < n; ++i) array.push_back((i<<1) + 1);
  cout << "Before transform:\n";
  copy(array.begin(), array.end(), ostream_iterator<int>(cout, ", "));
  cout << endl;
  TransWholeArray(array, n);
  cout << "After transform:\n";
  copy(array.begin(), array.end(), ostream_iterator<int>(cout, ", "));
  cout << endl;
  cout << "Transform is " << (Check(array) ? "OK." : "WRONG.") << endl;
  return 0;
}
